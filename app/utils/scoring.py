import re
import pandas as pd
import numpy as np

def calculate_cv_score(cv_text, keywords_dict):
    score = 0
    key_words = {}
    key_score = {}
    key_type = {}

    # Convertir le texte du CV en minuscules pour une correspondance insensible à la casse
    cv_text_lower = cv_text.lower()

    # Parcourir le dictionnaire des mots clés
    for keyword, data in keywords_dict.items():
        # Utiliser une expression régulière pour trouver toutes les occurrences des mots clés et de leurs synonymes
        pattern = re.compile(fr'\b(?:{"|".join(map(re.escape, data["synonyms"]))})\b')
        matches = pattern.findall(cv_text_lower)

        # Ajouter le score en fonction du nombre d'occurrences trouvées, multiplié par le score d'importance
        score += len(set(matches)) * data["score"]
        key_words[keyword] = list(set(matches))
        key_score[keyword] = len(set(matches)) * data["score"]
        key_type[keyword] = data["type"]

    return score, key_words, key_score, key_type

def compare_skill_importance(df_skills, df_words, major_val=33):
    def get_ranked_skills(df):
        return df.sort_values(by='Frequency in %', ascending=False).reset_index(drop=True)

    def check_same_order(df1, df2):
        return df1['Role'].equals(df2['Role'])

    def check_same_highest_skill(df1, df2):
        return df1.iloc[0]['Role'] == df2.iloc[0]['Role']

    def has_major_skill(df):
        max_freq=df['Frequency in %'].max()
        try:
            major_skill_list = (df[df['Frequency in %'] == max_freq].loc[:,"Role"].iloc[:]).tolist()
            if len(major_skill_list)>=1:
                major_skill=" & ".join([my_val for my_val in major_skill_list])
            else:
                major_skill=major_skill_list[0]
        except:
            major_skill = "no major"
        return  major_skill

    rank_df_skills = get_ranked_skills(df_skills)
    rank_df_words = get_ranked_skills(df_words)

    same_order = check_same_order(rank_df_skills, rank_df_words)
    same_highest_skill = check_same_highest_skill(rank_df_skills, rank_df_words)

    major_df_skills = has_major_skill(rank_df_skills)
    major_df_words = has_major_skill(rank_df_words)

    return same_order, same_highest_skill, major_df_skills, major_df_words

def contact_score(feat_cv_dict,max_score=5):
    contact_score=0
    if feat_cv_dict["email"]=='email not found':
        if has_word_in_urls(feat_cv_dict["urls"], "mailto")==True:
            contact_score+=1
    else:
        contact_score+=1

    if feat_cv_dict['other_phone']=='other phone not found':
        if feat_cv_dict['french_phone'] != 'French phone not found':
            contact_score += 1
    else:
        if feat_cv_dict['french_phone'] != 'French phone not found':
            contact_score+=1

    if feat_cv_dict["has_github"]=='github not mentionned':
        if has_word_in_urls(feat_cv_dict["urls"], "github")==True:
            contact_score+=1
    else:
        contact_score+=1

    if feat_cv_dict['has_linkedin']=='linkedin not mentionned':
        if has_word_in_urls(feat_cv_dict["urls"], "linkedin")==True:
            contact_score+=1
    else:
        contact_score+=1

    if len(feat_cv_dict["urls"])>0:
        contact_score+=1

    feat_cv_dict["raizuum_score_contact"]=contact_score
    feat_cv_dict["raizuum_score_contact_pc"] = round(contact_score/max_score*100,0)

    return feat_cv_dict

def section_score(feat_cv_dict,max_score=2):
    section_score=0
    if feat_cv_dict["score"]["role"]>0:
        section_score+=1
    if feat_cv_dict["score"]["studies"]>0:
        section_score+=1

    feat_cv_dict["raizuum_score_section"]=section_score
    feat_cv_dict["raizuum_score_section_pc"] = round(section_score/max_score*100,0)

    return feat_cv_dict

def role_skills_cv(feat_cv_dict, keywords_dict):
    #list where score is null and where score is the best
    role_skills_scores={"da":0, "de": 0, "ds":0}
    for my_key in keywords_dict:
        for the_role in ["da","de","ds"]:
            if the_role in keywords_dict[my_key]["subtype"]:
                try:
                    role_skills_scores[the_role]+=feat_cv_dict[my_key]["score"]
                except:
                    pass

    return role_skills_scores

def clear_role_score(feat_cv, keywords_dict_ds, max_score=4):
    clear_role_score=0
    role_skills_score = role_skills_cv(feat_cv, keywords_dict_ds)
    df_role_skills = role_feat_cv(role_skills_score)

    role_words_score = role_word_cv(feat_cv, keywords_dict_ds)
    df_role_words = role_feat_cv(role_words_score)

    same_order, same_highest_skill, major_df_skills, major_df_words = compare_skill_importance(df_role_skills,
                                                                                               df_role_words)
    if same_order:
        clear_role_score+=1
    if same_highest_skill:
        clear_role_score+=1
    if major_df_skills!="no major":
        clear_role_score += 1
    if major_df_words!="no major":
        clear_role_score += 1

    feat_cv["raizuum_score_role"]=clear_role_score
    feat_cv["raizuum_score_role_pc"] = round(clear_role_score/max_score*100,0)

    feat_cv["same_order"]= same_order
    feat_cv["same_highest_skill"]= same_highest_skill
    feat_cv["major_df_skills"] = major_df_skills
    feat_cv["major_df_words"] = major_df_words
    #feat_cv["df_role_skills"]=df_role_skills
    #feat_cv["df_role_words"] = df_role_words

    return feat_cv

def skills_score(feat_cv,max_score=6):
    skills_score=0
    if feat_cv["score"]["hard"] > 30:
        skills_score+=1
    if feat_cv["score"]["hard"] > 60:
        skills_score += 1
    if feat_cv["score"]["hard"] > 90:
        skills_score += 1
    if feat_cv["score"]["soft"] > 4:
        skills_score += 1
    if feat_cv["score"]["soft"] > 8:
        skills_score += 1
    if feat_cv["score"]["soft"] > 12:
        skills_score += 1

    feat_cv["raizuum_score_skills"]=skills_score
    feat_cv["raizuum_score_skills_pc"] = round(skills_score/max_score*100,0)

    return feat_cv

def readability_score(feat_cv, max_score=7):
    read_score=0
    if feat_cv["word_numbers"]>0:
        read_score+=1
    if feat_cv["page_numbers"]<=2:
        read_score+=1
    if feat_cv['word_numbers']>350 and feat_cv['word_numbers']<600:
        read_score+=1
    if feat_cv["num_bullet_points"]>0:
        read_score += 1
        if feat_cv["long_bullet_nb"]/feat_cv["num_bullet_points"]*100<20:
            read_score+=1
    if feat_cv["pronouns_nbr"]<=3:
        read_score+=1
    if feat_cv["cut_words_nbr"]==0:
        read_score+=1

    feat_cv["raizuum_score_read"]=read_score
    feat_cv["raizuum_score_read_pc"] = round(read_score/max_score*100,0)

    return feat_cv

def impact_score(feat_cv, max_score=6):
    impact_score=0
    if len(feat_cv["impact_numbers"])>0:
        impact_score+=1
    if len(feat_cv["impact_numbers"])>3:
        impact_score+=1
    if len(feat_cv["impact_numbers"])>8:
        impact_score+=1
    if feat_cv["nbr_experiences"]>0:
        if len(feat_cv["impact_numbers"]) / feat_cv["nbr_experiences"]/2>0.5:
            impact_score+=1
        if len(feat_cv["impact_numbers"]) / feat_cv["nbr_experiences"]/2>0.8:
            impact_score+=1
        if len(feat_cv["impact_numbers"]) / feat_cv["nbr_experiences"]/2 >= 1:
            impact_score += 1

    feat_cv["raizuum_score_impact"]=impact_score
    feat_cv["raizuum_score_impact_pc"] = round(impact_score/max_score*100,0)

    return feat_cv

def comp_total_score(feat_cv, max_score=30):
    total_score = (feat_cv["raizuum_score_contact"] + feat_cv["raizuum_score_section"] +
                   feat_cv["raizuum_score_role"] + feat_cv["raizuum_score_skills"] +feat_cv["raizuum_score_read"] + feat_cv["raizuum_score_impact"])

    feat_cv["raizuum_score_total"] = total_score
    feat_cv["raizuum_score_total_pc"] = round(total_score / max_score * 100, 0)

    return feat_cv

def test_filename(the_filename):
    #Test the Resume filename and give a score
    filename_test_results={}
    filename_test_results["filename"]=the_filename
    filename_test_results["filen_woext"]="".join([my_val for my_val in the_filename.split('.')[:-1]])
    #test 1 : separator
    sep_list=["_","-"]
    results_sep=len([char for char in filename_test_results["filen_woext"] if char in sep_list])
    if results_sep>0:
        filename_test_results["separator"]="✅ Good Separator Choice"
    else:
        filename_test_results["separator"]="⛔ Review separator Choice"

    #test 2 : spaces
    results_sep=len([char for char in filename_test_results["filen_woext"] if char==" "])
    if results_sep==0:
        filename_test_results["spaces"]="✅ No spaces detected"
    else:
        filename_test_results["spaces"]="⛔ Remove blank spaces from filename"

    #test 2 : title
    title_list=["datascientist","dataanalyst","dataengineer","da","ds","de","data"]
    results_title=len([title for title in title_list if title in filename_test_results["filen_woext"].lower()])
    if results_title>0:
        filename_test_results["title"]="✅ Good mention of your job title"
    else:
        filename_test_results["title"]="⛔ We did not find your data job title"

    #test length
    if len(filename_test_results["filen_woext"])>50:
        filename_test_results["length"] = "⛔ Can you make it shorter ?"
        filename_test_results["length"] = "✅ Proper length"
    elif len(filename_test_results["filen_woext"])<8:
        filename_test_results["length"] = "⛔ Seems very short to be memorable ?"
    else:
        filename_test_results["length"] = "✅ Proper length"

    #test numeric
    results_num=len([char for char in filename_test_results["filen_woext"] if char.isnumeric()])
    if results_num==0:
        filename_test_results["numeric"]="✅ No numbers detected"
    else:
        filename_test_results["numeric"]="⛔ Remove any numeric character (versions, dates...)"

    #test special characters
    # Regex to detect emojis and non-ASCII characters (including accents)
    pattern = r'[^\x00-\x7F]'

    # Find all special characters, emojis, or accented characters
    results_special = re.findall(pattern, filename_test_results["filen_woext"])
    if len(results_special)==0:
        filename_test_results["specialChar"]="✅ No special characters or Emoji detected"
    else:
        filename_test_results["specialChar"]="⛔ Remove any special characters or Emoji"

    return filename_test_results

def rate_feat_cv(feat_cv_dict, keywords_dict, the_type='hard'):
    #list where score is null and where score is the best
    null_list=[]
    best_list=[]
    role_list=[]
    for my_key in keywords_dict:
        if feat_cv_dict[my_key]["type"]==the_type:
            try:
                score=feat_cv_dict[my_key]["score"]
                if score==0:
                    null_list.append([my_key,keywords_dict[my_key]["score"]])
                if score>0:
                    best_list.append([my_key,feat_cv_dict[my_key]["score"]])
            except:
                pass

    return sorted(null_list, key=lambda x: x[1])[::-1], sorted(best_list, key=lambda x: x[1])

def role_word_cv(feat_cv_dict, keywords_dict):
    #list where score is null and where score is the best
    role_word_scores={"da":0, "de": 0, "ds":0}
    for my_key in keywords_dict:
        for the_role in ["da", "de", "ds"]:
            if feat_cv_dict[my_key]["type"]=="role" and the_role in keywords_dict[my_key]["subtype"]:
                try:
                    role_word_scores[the_role] += feat_cv_dict[my_key]["score"]
                except:
                    pass

    return role_word_scores

def role_feat_cv(role_score):
    role_score_ok=[]
    total = sum([role_score[val] for val in role_score])
    role_score_ok.append({"Role":"Data Analyst","Frequency in %" : int(role_score["da"]/(total+0.01)*100)})
    role_score_ok.append({"Role":"Data Engineer","Frequency in %" : int(role_score["de"] / (total + 0.01)*100)})
    role_score_ok.append({"Role":"Data Scientist", "Frequency in %" : int(role_score["ds"] / (total + 0.01)*100)})
    df_role = pd.DataFrame.from_dict(role_score_ok)
    return df_role

def studies_feat_cv(feat_cv_dict, keywords_dict):
    #list where score is null and where score is the best
    studies_list=[]
    for my_key in keywords_dict:
        if feat_cv_dict[my_key]["type"]=="studies":
            try:
                score = feat_cv_dict[my_key]["score"]
                if score>0:
                    studies_list.append([my_key,feat_cv_dict[my_key]["words"]])
            except:
                pass

    return studies_list

