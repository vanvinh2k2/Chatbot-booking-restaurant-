import spacy
from .synonyms import synonyms
nlp = spacy.load("en_core_web_sm")

def getName(text):
    doc = nlp(text)
    proper_nouns = []
    current_proper_noun = ""
    for token in doc:
        if token.pos_ == "PROPN":
            current_proper_noun += " " + token.text
        else:
            if current_proper_noun.strip():
                proper_nouns.append(current_proper_noun.strip())
                current_proper_noun = ""

    # Kiểm tra nếu còn từ riêng cuối cùng trong văn bản
    if current_proper_noun.strip():
        proper_nouns.append(current_proper_noun.strip())
    return proper_nouns


def getRole(a, text):
    synonyms_res = synonyms("restaurant")
    synonyms_dish = synonyms("dish")

    for word in synonyms_res:
        text1 = a + " " + word.replace("_", " ")
        text2 = word.replace("_", " ") + " " + a
        if text1 in text or text2 in text:
            return True
        
    for word in synonyms_dish:
        text1 = a + " " + word.replace("_", " ")
        text2 = word.replace("_", " ") + " " + a
        if text1 in text or text2 in text:
            return False

    return None
    
