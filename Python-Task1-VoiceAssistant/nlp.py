import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

from intents import intents


# Stemmer
stemmer = PorterStemmer()


# Common words that don't help identify the intent
stop_words = {
    "a", "an", "the", "is", "are", "am",
    "can", "could", "would", "you", "me",
    "please", "tell", "to", "for", "of",
    "do", "does", "did", "i", "want",
    "my", "it", "today",
    "now", "some"
}


# Convert sentence into useful words
def tokenize(sentence):

    words = word_tokenize(sentence.lower())

    useful_words = []

    for word in words:

        if word.isalpha() and word not in stop_words:

            stemmed_word = stemmer.stem(word)

            useful_words.append(stemmed_word)

    return useful_words


# Calculate similarity
def calculate_similarity(user_words, example_words):

    user_words = set(user_words)
    example_words = set(example_words)

    if not user_words or not example_words:
        return 0

    common_words = user_words.intersection(example_words)

    # Compare against the smaller set
    score = len(common_words) / min(
        len(user_words),
        len(example_words)
    )

    return score


# Predict intent
def predict_intent(sentence):

    user_words = tokenize(sentence)

    best_intent = "unknown"
    best_score = 0

    for intent, examples in intents.items():

        for example in examples:

            example_words = tokenize(example)

            score = calculate_similarity(
                user_words,
                example_words
            )

            if score > best_score:
                best_score = score
                best_intent = intent


    if best_score < 0.30:
        return "unknown"

    return best_intent
