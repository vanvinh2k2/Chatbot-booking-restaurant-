import nltk
from nltk.corpus import stopwords, wordnet
nltk.download('stopwords')
from nltk.stem import WordNetLemmatizer
import spacy
nlp = spacy.load("en_core_web_sm")

def singular_to_plural(word):
    lemmatizer = WordNetLemmatizer()
    plural_form = lemmatizer.lemmatize(word, pos='n')
    if plural_form != word.lower():
        return plural_form
    else:
        doc = nlp(word)
        # Lấy từ gốc của từ động từ
        lemma = doc[0].lemma_
        return lemma

def remove_stopwords(sentence):
    stop_words = set(stopwords.words('english'))
    words = sentence.split()
    filtered_words = [word for word in words if word not in stop_words]
    filtered_sentence = ' '.join(filtered_words)
    filtered_words2 = []
    for word in filtered_sentence.split():
        plural_form = singular_to_plural(word)
        if plural_form is not None:
            filtered_words2.append(plural_form)
        else: filtered_words2.append(word)
    filtered_sentence = ' '.join(filtered_words2)
    return filtered_sentence
    