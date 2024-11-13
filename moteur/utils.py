import re

def clear_text(text):
    return re.sub(r"\s+", " ", text).strip()

def extract_number(string):
    return int(re.sub(r"[^\d]", "", string))
