from utils.skills_extractor import extract_skills

def calculate_ats_score(resume_skills, jd_text):
    jd_skills = extract_skills(jd_text)
    matched = set(resume_skills).intersection(set(jd_skills))
    if len(jd_skills) == 0:
        return 0
    score = int((len(matched) / len(jd_skills)) * 100)
    return score

def predict_chance(score, experience):
    if score >= 80 and experience >= 2:
        return "High (85%)"
    elif score >= 60:
        return "Moderate (60%)"
    else:
        return "Low (35%)"
