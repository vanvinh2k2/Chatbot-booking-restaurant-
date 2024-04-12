from nltk.corpus import wordnet
from .customer_word import remove_stopwords
import re

def synonyms(word):
        synonyms = set()
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonyms.add(lemma.name())
        return synonyms
    
def search_word(words, data_set, check):
    for word in words:
        kt = False
        synonyms_words = synonyms(word)
        for synonym_word in synonyms_words:
            if "_" in synonym_word: 
                synonym_word = remove_stopwords(synonym_word.replace("_", " "))
            if re.search(r"\b"+synonym_word+r"\b", data_set, re.IGNORECASE):
                kt = True
                break
        if kt == False:
            check = False
    return check