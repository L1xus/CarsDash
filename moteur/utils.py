import re

def clear_text(text):
    return re.sub(r"\s+", " ", text).strip()
