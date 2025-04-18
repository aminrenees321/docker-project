import re

def extract_experience(text):
    matches = re.findall(r'(\d+)\+?\s*(years|yrs)', text.lower())
    total_exp = sum(int(year[0]) for year in matches)
    return total_exp
