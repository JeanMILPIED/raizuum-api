import re
from collections import Counter

def remove_accents(input_str):
    # Define a regular expression to match accented characters
    pattern = re.compile('[\u0300-\u036f]')

    # Use re.sub to replace accented characters with empty string
    result = re.sub(pattern, '', input_str)

    return result

def count_most_frequent_words(text, num_words=10, min_length=4):
    linking_words = set([
        # English linking words
        "and", "or", "but", "nor", "so", "for", "yet", "after", "although", "as", "because",
        "before", "even if", "even though", "if", "in order that", "once", "provided that",
        "rather than", "since", "so that", "than", "that", "though", "unless", "until",
        "when", "whenever", "where", "whereas", "wherever", "whether", "while",
        "about", "above", "across", "after", "against", "along", "among", "around", "at",
        "before", "behind", "below", "beneath", "beside", "between", "beyond", "by",
        "despite", "down", "during", "except", "for", "from", "in", "inside", "into",
        "like", "near", "of", "off", "on", "out", "over", "past", "since", "through",
        "throughout", "to", "toward", "under", "until", "up", "upon", "with", "within", "without",
        # French linking words
        "ainsi", "et", "ou", "mais", "ni", "donc", "car", "alors", "apres", "avant", "bien que",
        "comme", "parce que", "puisque", "quand", "lorsque", "pendant", "depuis", "pour",
        "sans", "sous", "sur", "chez", "dans", "entre", "par", "avec", "contre", "de", "en",
        "jusqu'a", "malgre", "vers", "selon", "au", "aux", "du", "des", "chez", "l'", "d'",
        "pour", "afin de", "parce que", "quoique", "si", "tandis que", "quoi que", "ou"
    ])

    # Use regex to find words, ignoring punctuation and case
    words = re.findall(r'\b\w+\b', text.lower())

    # Filter words based on minimum length
    filtered_words = [word for word in words if ((len(word) >= min_length) and (word not in linking_words) and (
        not any(char.isdigit() for char in word)))]

    # Count the frequency of each word
    word_counts = Counter(filtered_words)

    # Get the most common words
    most_common_words = word_counts.most_common(num_words)

    return most_common_words

def human_reading(num_words, wpm=200):
    # Estimate reading duration
    duration_minutes = num_words / wpm
    duration_seconds = duration_minutes * 60
    return int(duration_seconds)

def find_pronouns(text):
    # Define the pronouns to search for
    pronouns = ['I', 'i','We','we', 'They','they', 'You','you', 'Je','je' 'Tu', 'tu', 'Il','il', 'Nous','nous' 'Vous','vous', 'Ils','ils', 'Elles','elles',"j'","J'"]

    # Compile a regex pattern for case-insensitive matching with word boundaries
    pattern = re.compile(r'\b(?:-|\s|^)?(' + '|'.join(pronouns) + r"|j')\b", re.IGNORECASE)

    # Find all matches in the input text
    matches = pattern.findall(text)


    # Normalize matches to the correct capitalization
    matches = [match.capitalize() for match in matches]
    pronoun_nbr=len(matches)

    #count the most frequent ponouns
    pronoun_counts = Counter(matches)
    # Return the list of matched pronouns
    return pronoun_counts, pronoun_nbr

def find_cut_words(text):
    # Compile a regex pattern for cut words
    pattern = re.compile(r'\b\w+-\s+\w+\b', re.IGNORECASE)

    # Find all matches in the input text
    matches = pattern.findall(text)

    # Filter out date-like patterns
    filtered_matches = [
        match for match in matches
        if not re.search(r'\b\d{4}\b', match) and
           not re.search(r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b', match, re.IGNORECASE)]

    # Return the list of matched cut words
    return filtered_matches

def word_numbers(text):
    word_numbers = len([s for s in re.split("[() ,|;\W]+", text)])
    return word_numbers
