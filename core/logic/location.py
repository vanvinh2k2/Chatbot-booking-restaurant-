from underthesea import ner
from const.location import vietnam_provinces, english_provinces
from unidecode import unidecode

def extract_location(sentence):
    locations = []
    entities = ner(sentence)
    print(entities)
    for entity in entities:
        if unidecode(entity[0]) in english_provinces:
            locations.append(entity[0])
    return locations

# Example usage
sentence = "Nhà hang ở Da nang hoặc HCM mở cửa lúc mấy giờ?"
# sentence = "Địa chỉ cảu nhà hàng New Time"
locations = extract_location(sentence)
print("Địa điểm:", locations)
