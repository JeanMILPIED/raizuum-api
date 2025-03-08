import re

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