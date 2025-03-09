import re
from spellchecker import SpellChecker
import unicodedata

def extract_impact(text):
    # Define a regex pattern to match numbers followed by %
    pattern1 = r'\S*%'

    # Use re.findall to extract all matches in the text
    matches1 = re.findall(pattern1, text, re.IGNORECASE)
    # Extracted numbers with their respective symbols
    #we keep only short numbers
    results1 = [res_match for res_match in matches1 if len(str(res_match))<10]

    # Define a regex pattern to match €
    pattern2 = r'\S*€'
    # Use re.findall to extract all matches in the text
    matches2 = re.findall(pattern2, text, re.IGNORECASE)
    results2 =matches2

    # Define a regex pattern to match $
    pattern3 = r'\S*\$'
    # Use re.findall to extract all matches in the text
    matches3 = re.findall(pattern3, text, re.IGNORECASE)
    results3 = matches3

    # Define a regex pattern to match Go Mo To
    pattern4 = [r'\b\d+Go\b',r'\b\d+Mo\b',r'\b\d+To\b',r'\b\d+Ko\b']
    # Use re.findall to extract all matches in the text
    matches4=[]
    for reg in pattern4:
        matches4 +=re.findall(reg, text, re.IGNORECASE)
    results4 =matches4

    # Define a regex pattern to match time units
    pattern5 = [
        r'\b\d+\s?ms\b',  # Matches "10ms", "0.5ms"
        r'\b\d+\s?minutes?\b',  # Matches "10minute", "10minutes"
        r'\b\d+\s?hours?\b',  # Matches "10hour", "10hours"
        r'\b\d+\s?heures?\b',  # Matches "10heure", "10heures"
        r'\b\d+\s?jours?\b',  # Matches "10jour", "10jours", "0.65 jour"
        r'\b\d+\s?days?\b'  # Matches "10day", "10days"
    ]
    # Use re.findall to extract all matches in the text
    matches5=[]
    for reg in pattern5:
        matches5 +=re.findall(reg, text, re.IGNORECASE)
    results5 =matches5

    #get action verbs
    # Expand the list of action or impact verbs
    action_verbs = {
        'english': [
            "enhance", "achieved", "achievement", "affected", "altered", "amplified", "amplification", "built",
            "changed", "change", "constructed", "construction",
            "created", "creation", "damaged", "decreased", "decrease", "destroyed", "destruction", "developed",
            "development", "enhanced",
            "enforced", "established", "generated", "generation", "improved", "improvement", "influenced",
            "increased", "increase", "initiated", "initiation", "innovated", "innovation", "launched", "launch",
            "maintained",
            "modified", "modification", "neglected", "produced", "production", "reduced", "reduction", "reinforced",
            "reinforcement", "shaped", "transformed", "transformation",
            "adapted", "adaptation", "advanced", "advancement", "boosted", "boost", "controled", "control", "corrected",
            "correction", "designed", "design",
            "driven", "executed", "executin", "facilitated", "facilitation", "fostered", "guided", "implemented",
            "implementation",
            "initiated", "initiation", "managed", "management", "optimized", "optimisation", "planed", "promoted",
            "promotion", "strengthened",
            "supported", "sustained"
        ],
        'french': [
            "automatisé", "automatisation", "accéléré", "accélération", "accompli", "accomplissement", "affecté",
            "amélioré", "amélioration", "amplifié", "amplification", "augmenté", "augmentation",
            "bâti", "changé", "changement", "conçu", "conception", "construit", "construction", "créé", "création",
            "détruit", "destruction", "développé", "développement",
            "diminué", "diminution", "élaboré", "élaboration", "encouragé", "encouragement", "renforcé", "renforcement",
            "établi", "établissement", "généré", "génération",
            "influencé", "influence", "innové", "innovation", "lancé", "lancement", "maintenu", "maintien", "modifié",
            "modification", "négligé",
            "produit", "production", "réduit", "réduction", "transformé", "transformation", "adapté", "adaptation",
            "avancé", "avancement",
            "boosté", "boost", "contrôlé", "contrôle", "corrigé", "correction", "dessiné", "exécuté", "exécution",
            "facilité", "facilitation", "favorisé", "guidé", "implémenté", "implémentation", "initié", "initiation",
            "optimisé", "optimisation", "planifié", "planification", "promu", "promotion", "soutenu", "soutien",
            "entretenu", "entretien", "réaliser", "réalisation"
        ]
    }

    # Normalize text: Remove accents for matching
    def normalize_text(text: str) -> str:
        return ''.join(
            c for c in unicodedata.normalize('NFD', text)
            if unicodedata.category(c) != 'Mn'
        )

    # Function to search for verbs in text
    def find_verbs(text: str, action_verbs: dict[str, list[str]]) -> list[str]:
        text = text.lower()  # Lowercase the text for case-insensitive matching
        found_verbs = set()

        # Normalize verbs by removing accents (if any) and update the dictionary
        normalized_verbs = {lang: [normalize_text(verb) for verb in verbs] for lang, verbs in action_verbs.items()}

        for lang, verbs in normalized_verbs.items():
            for verb in verbs:
                # Create regex pattern to match different verb conjugations
                pattern = r'\b' + re.escape(verb) + r'(e?s?|ed|ing|ant|e|es|ons|er|ait|ions|ent)?\b'
                matches = re.findall(pattern, text)
                if matches:
                    found_verbs.add(verb)

        return list(found_verbs)

    results_nouns = find_verbs(text, action_verbs)

    return results1 + results2 + results3 + results4 + results5 + results_nouns

def extract_email(text):
    # get email
    match_email= re.search('[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',text)
    return match_email

def extract_french_phone(text):
    match_fr_phone = re.search(
        '(?:(?:\+|00)33[\s.-]{0,3}(?:\(0\)[\s.-]{0,3})?|0)[1-9](?:(?:[\s.-]?\d{2}){4}|\d{2}(?:[\s.-]?\d{3}){2})',
        text)
    return match_fr_phone

def extract_any_phone(text):
    mob_num_regex = r'''(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)
                    [-\.\s]*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'''
    match_any_phone = re.findall(re.compile(mob_num_regex), text)
    return match_any_phone

def extract_github(text):
    #FIXME: format is not good
    response = {}
    # get github account
    if 'github' in text:
        response['has_github']='github'
        match_github= re.search('https://github.com+[/a-zA-Z0-9]+',text)
        if match_github:
            response['github_account']=match_github.group()
        else:
            response['github_account']='github account not found'
    else:
        response['has_github']='github not mentionned'
        response['github_account']='github account not found'
    return response

def extract_likedin(text):
    # FIXME: format is not good
    response={}
    # get linkedin account
    if 'linkedin' in text:
        response['has_linkedin']='linkedin'
    else:
        response['has_linkedin']='linkedin not mentionned'
    return response

def extract_dates(text):
    # Regular expression pattern to match dates in various formats
    year_pattern = r'\b(19\d{2}|20\d{2})\b'
    # Find all dates in the text using the regex pattern
    dates = re.findall(year_pattern, text)
    #we keep dates over 1980
    dates=[my_date for my_date in dates if int(my_date) >=2000]
    return dates

def get_min_max_dates(dates):
    try:
        # Find minimum and maximum dates
        min_date = min(dates)
        max_date = max(dates)
    except:
        min_date, max_date = 0, 0
    return min_date, max_date

def analyze_bullets_text(text, max_length=30):
    # Find all bullet points and the text following them until the next bullet point or end of text
    bullet_points = re.findall(r'^[\s]*[-•*●–—▪]+[\s]+(.*?)(?=(\n[\s]*[-•*●–—▪])|\Z)', text, re.DOTALL | re.MULTILINE)

    bullet_points_text = [bp[0].strip() for bp in bullet_points]
    bullet_point_lengths = [len(bp.split()) for bp in bullet_points_text]
    num_bullet_points = len(bullet_points_text)

    numb_max = len([my_val for my_val in bullet_point_lengths if my_val > max_length])

    return num_bullet_points, bullet_point_lengths, numb_max


def check_typos(text):
    spell_uk = SpellChecker()
    spell_fr = SpellChecker(language='fr')

    special_chars_pattern = re.compile(r'[\W_]+')
    # Remove special characters (excluding spaces)
    text = re.sub(special_chars_pattern, ' ', text)

    # Split by space or single quote ('), using regular expression
    words = re.split(r'\s+|\'|\’|\(|\)|:|-|_|,', text)
    # Remove empty strings from the result
    words = [word for word in words if ((word != "") & (len(word) > 3) & (not any(char.isupper() for char in word)) & (
        not any(char.isdigit() for char in word)))]
    typos = []
    for word in words:
        if (word not in spell_fr) & (word not in spell_uk) & (word not in typos):
            # correction_fr = spell_fr.correction(word)
            # correction_uk = spell_uk.correction(word)
            typos.append(word)
            # typos_list.append(word)
    return typos

def extract_urls(text):
    url_pattern = re.compile(r'https?://\S+')
    return url_pattern.findall(text)