import os
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
from fastapi import UploadFile
import tempfile
from app.utils.extractor import *
from app.utils.nlp_utils import *
from app.utils.scoring import *



def extract_text_by_page(pdf_path):
    """
    Extract text from a PDF file, returning a list of strings where each string is the text of a single page.

    :param pdf_path: Path to the PDF file.
    :return: List of strings, each representing the text of a page.
    """
    pages_text = []

    for page_layout in extract_pages(pdf_path):
        page_text = ""
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                page_text += element.get_text()
        pages_text.append(page_text)

    return pages_text


async def process_pdf(file: UploadFile):
    """
    Handles an uploaded PDF, extracts text, and returns structured data.

    :param file: UploadedFile from FastAPI.
    :return: Extracted text as a list of pages.
    """
    # Save uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(await file.read())
        tmp_pdf_path = tmp_file.name

    # Extract text
    text_pages = extract_text_by_page(tmp_pdf_path)

    # Delete temporary file after processing
    os.remove(tmp_pdf_path)

    return text_pages


def get_features_text_cv(my_text, keywords_dict, cv_feat_dict={}):
    cv_feat_dict['page_numbers'] = len(my_text)
    # we analyse only page 1
    # my_text=my_text[0]
    my_text = '\n'.join(my_text)
    cv_feat_dict['line_numbers'] = my_text.count('\n')

    # extract paragraph stats
    num_bullet_points, bullet_point_lengths, numb_max = analyze_bullets_text(my_text)
    cv_feat_dict["num_bullet_points"] = num_bullet_points
    cv_feat_dict["bullet_point_lengths"] = bullet_point_lengths
    cv_feat_dict["long_bullet_nb"] = numb_max

    my_text = my_text.replace('\n', ' ')
    my_text = re.sub(r' +', ' ', my_text)
    my_text_ok = remove_accents(my_text)

    # count_1
    count_1 = len([1 for my_word in my_text_ok.split() if len(my_word) == 1])
    pc_1 = count_1 / len(my_text_ok.split())
    if pc_1 > 0.99:
        my_text_ok = my_text_ok.replace(' ', '')

    cv_feat_dict['word_numbers'] = len([s for s in re.split("[() ,|;\W]+", my_text_ok)])

    my_text_ok = my_text_ok.lower()

    # remove accents
    repl = str.maketrans("àâéèêëûôöïç", "aaeeeeuooic")
    my_text_ok = my_text_ok.translate(repl)

    # get email
    match_email = re.search('[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', my_text_ok)
    if match_email:
        cv_feat_dict['email'] = match_email.group()
    else:
        cv_feat_dict['email'] = 'email not found'

    # get phone number
    match_fr_phone = re.search(
        '(?:(?:\+|00)33[\s.-]{0,3}(?:\(0\)[\s.-]{0,3})?|0)[1-9](?:(?:[\s.-]?\d{2}){4}|\d{2}(?:[\s.-]?\d{3}){2})',
        my_text_ok)
    if match_fr_phone:
        cv_feat_dict['french_phone'] = match_fr_phone.group()
    else:
        cv_feat_dict['french_phone'] = 'French phone not found'

    # match_any_phone= re.search('[\+]?[\(]?[0-9]{2,3}[)]?[-\s\.]?[0-9]{2,3}[-\s\.]?[0-9]{3,6}[-\s\.]?[0-9]{3,6}',my_text_ok)
    mob_num_regex = r'''(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)
                    [-\.\s]*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'''
    match_any_phone = re.findall(re.compile(mob_num_regex), my_text_ok)
    if match_any_phone:
        cv_feat_dict['other_phone'] = ''.join(match_any_phone[0])
    else:
        cv_feat_dict['other_phone'] = 'other phone not found'

    # get github account
    if 'github' in my_text_ok:
        cv_feat_dict['has_github'] = 'github'
        match_github = re.search('https://github.com+[/a-zA-Z0-9]+', my_text_ok)
        if match_github:
            cv_feat_dict['github_account'] = match_github.group()
        else:
            cv_feat_dict['github_account'] = 'github account not found'
    else:
        cv_feat_dict['has_github'] = 'github not mentionned'
        cv_feat_dict['github_account'] = 'github account not found'

    # get linkedin account
    if 'linkedin' in my_text_ok:
        cv_feat_dict['has_linkedin'] = 'linkedin'
    else:
        cv_feat_dict['has_linkedin'] = 'linkedin not mentionned'

    # count key words from a competence list
    list_keycomp = ['ia ', 'ai ', 'data', 'datascience', 'data scienc', 'datascient', 'data eng', 'python', ' r ',
                    'sql', 'docker', 'cloud', 'aws', 'azure', 'google', 'gcp', 'ml', 'algorithm', 'algo', 'statisti',
                    'keras', 'pytorch', 'machine learning', 'tensorflow', 'opencv', 'computer vision', 'pandas',
                    'numpy', 'nlp', 'dl ', 'deeplearning', 'deep learn', 'neural net', 'neuron', 'time serie',
                    'anomaly', 'llm', 'prompt', 'spark']
    cv_feat_dict['the_data_comp'] = [my_comp for my_comp in list_keycomp if my_comp in my_text_ok]

    # count key words from a diploma list
    list_keydiploma = ['phd', 'docteur', 'master', 'iut', 'dut', 'ingenie', 'msc', 'bac', 'license', 'maitrise',
                       'master2', 'ecole', 'école', 'superieu', 'reconvers']
    cv_feat_dict['the_data_diploma'] = [my_dipl for my_dipl in list_keydiploma if my_dipl in my_text_ok]

    # count key words from a language list
    list_keylang = ['francais', 'french', 'anglais', 'english', 'allemand', 'german', 'indien', 'indian', 'arabe',
                    'arabic', 'espagnol', 'spanish', 'italien', 'italian', 'chinois', 'chinese']
    cv_feat_dict['the_data_lang'] = [my_lang for my_lang in list_keylang if my_lang in my_text_ok]

    # count manager experience
    list_keymgt = ['management', 'manageur', 'manager', 'team', 'equipe', 'mgr ', 'agile', 'sprint']
    cv_feat_dict['the_data_mgt'] = [my_mgt for my_mgt in list_keymgt if my_mgt in my_text_ok]

    # compute score
    list_kw = []
    total_score, extract_words, extract_score, extract_type = calculate_cv_score(my_text_ok, keywords_dict)
    for keyw in extract_words:
        interim_dict = {"words": extract_words[keyw], "score": extract_score[keyw], "type": extract_type[keyw]}
        cv_feat_dict[keyw] = interim_dict
        list_kw.append(keyw)

    cv_feat_dict["score"] = {}
    cv_feat_dict["score"]["total"] = total_score
    for the_type in ["hard", "soft", "role", "studies"]:
        cv_feat_dict["score"][the_type] = sum(
            [cv_feat_dict[keyw]["score"] for keyw in list_kw if cv_feat_dict[keyw]["type"] == the_type])

    # extract dates
    # Extract dates from the resume text
    dates = extract_dates(my_text_ok)
    cv_feat_dict["dates"] = {}
    cv_feat_dict["dates"]["all"] = dates
    # Get minimum and maximum dates
    min_date, max_date = get_min_max_dates(dates)
    cv_feat_dict["dates"]["min"] = min_date
    cv_feat_dict["dates"]["max"] = max_date
    cv_feat_dict["nbr_experiences"] = int((len(dates) + 1) / 2)

    # extract most frequent words
    most_fqt_words = count_most_frequent_words(my_text_ok)
    cv_feat_dict["most_frequent_words"] = most_fqt_words

    # extract frequent pronouns
    fqt_pronouns, pronouns_nbr = find_pronouns(my_text_ok)
    cv_feat_dict["frequent_pronouns"] = fqt_pronouns
    cv_feat_dict["pronouns_nbr"] = pronouns_nbr

    # extract cut words
    cut_words_list = find_cut_words(my_text_ok)
    cv_feat_dict["cut_words"] = cut_words_list
    cv_feat_dict["cut_words_nbr"] = len(cut_words_list)

    # extract typo words
    typos = check_typos(my_text)
    cv_feat_dict["typos"] = typos

    # extract impact numbers
    impact_numbers = extract_impact(my_text_ok)
    cv_feat_dict["impact_numbers"] = impact_numbers

    # get image features
    cv_feat_dict = get_features_pdf_cv('your_resume.pdf', 1, cv_feat_dict)

    # get contact score
    cv_feat_dict = contact_score(cv_feat_dict)

    # get section score
    cv_feat_dict = section_score(cv_feat_dict)

    # get role score
    cv_feat_dict = clear_role_score(cv_feat_dict, keywords_dict)

    # get skills score
    cv_feat_dict = skills_score(cv_feat_dict)

    # get read score
    cv_feat_dict = readability_score(cv_feat_dict)

    # get impact score
    cv_feat_dict = impact_score(cv_feat_dict)

    # get total score
    cv_feat_dict = comp_total_score(cv_feat_dict)

    # get match vector
    cv_feat_dict["match_vector"] = build_role_skills_impact_vector(cv_feat_dict)

    return my_text, cv_feat_dict

