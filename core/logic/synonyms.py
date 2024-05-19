from nltk.corpus import wordnet

def synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return synonyms

# word = "address"
# print(f"Các từ đồng nghĩa với '{word}': {synonyms(word)}")