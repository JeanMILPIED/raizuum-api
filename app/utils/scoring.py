import re

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

