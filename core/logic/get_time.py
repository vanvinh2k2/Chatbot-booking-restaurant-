import re
from .synonyms import synonyms
from .format_time import format_time

def extract_opening_hours(text):
    time_pattern = re.compile(r'\b\d{1,2}(?::\d{2})?(?:\s*(?:a\.m\.?|p\.m\.?))?\b', re.IGNORECASE)
    times = time_pattern.findall(text)
    
    if len(times) >= 2:
        opening_time = format_time(times[0])
        closing_time = format_time(times[1])
        return opening_time, closing_time
    elif len(times) == 1:
        time = format_time(times[0])
        open_words = synonyms("open")
        close_words = synonyms("close")
        for open_time in open_words:
            if open_time in text:
                return time, None
        for close_time in close_words:
            if close_time in text:
                return None, time
    else: return None, None

# question = "Restaurants close from 10 p.m"
# opening_hours = extract_opening_hours(question)
# if opening_hours:
#     opening_time, closing_time = opening_hours
#     print("Giờ mở cửa:", opening_time)
#     print("Giờ đóng cửa:", closing_time)
# else:
#     print("Không tìm thấy thời gian mở cửa trong câu hỏi.")
