def format_time(input_time):
    is_am_pm = False
    if "a.m" in input_time.lower() or "p.m" in input_time.lower(): is_am_pm = True
    if ":" in input_time and "p.m" not in input_time: formatted_time = input_time
    elif is_am_pm:
        if "p.m" in input_time.lower() and ":" not in input_time:
            hour = int(input_time.split(" ")[0])
            if hour != 12: hour += 12
        elif "p.m" in input_time.lower() and ":" in input_time:
            hour = int(input_time.split(":")[0])
            if hour != 12: hour += 12
        else: hour = int(input_time.split(" ")[0])
        formatted_time = f"{hour:02d}:00"
    else: formatted_time = input_time + ":00"
    return formatted_time[:5]

# times = ["10", "10 a.m", "10:00", "10:00 a.m", "8 p.m", "10:00 p.m"]
# for time in times:
#     formatted_time = format_time(time)
#     print(formatted_time)