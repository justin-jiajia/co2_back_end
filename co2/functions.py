from datetime import datetime


def now_time():
    time_now = datetime.now()
    time_now_string = f"{time_now.year}/{time_now.month}/{time_now.day}"
    return time_now_string
