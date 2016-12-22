__author__ = 'wenjusun'

from datetime import datetime
def normalize_str(str):
    if str:
        return str.strip()
    else:
        return ""


def get_now():
    return datetime.now()