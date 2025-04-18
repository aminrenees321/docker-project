import re

skills_list = [
    "python", "java", "c++", "sql", "excel", "machine learning",
    "jobs analysis", "communication", "teamwork", "leadership",
    "django", "flask", "streamlit", "html", "css", "javascript"
]

def extract_skills(text):
    found = []
    for skill in skills_list:
        if re.search(r'\b' + re.escape(skill) + r'\b', text.lower()):
            found.append(skill)
    return list(set(found))
