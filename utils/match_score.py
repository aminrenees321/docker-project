from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_match(cv_text, job_description):
    # Check for None or empty inputs
    if not cv_text or not job_description:
        raise ValueError("Both CV text and job description must be provided and cannot be empty.")

    vectorizer = TfidfVectorizer(stop_words='english')

    try:
        # Perform vectorization
        tfidf_matrix = vectorizer.fit_transform([cv_text, job_description])
    except Exception as e:
        raise ValueError(f"Error during TF-IDF vectorization: {e}")

    # Calculate cosine similarity
    cosine_similarities = (tfidf_matrix * tfidf_matrix.T).toarray()
    match_score = cosine_similarities[0][1]  # Similarity between CV and Job Description

    # Apply Bias
    if match_score < 0.5:
        biased_score = match_score + 0.2  # Increasing the score to be more favorable
    else:
        biased_score = min(1.0, match_score + 0.1)  # Adding a smaller bias for higher scores

    return round(biased_score * 100, 2)

def suggest_improvements(cv_text, job_description, score):
    suggestions = []

    # Basic suggestions based on the match score
    if score < 50:
        suggestions.append("➔ Your CV doesn't match the job description well. Focus on adding keywords related to the role.")
        suggestions.append("➔ Make sure your skills align with the job requirements. Consider learning missing skills.")
        suggestions.append("➔ Add more relevant experience and projects, ideally aligned with the job role.")
        suggestions.append("➔ Highlight key achievements and certifications that are relevant to the job description.")
    elif score < 70:
        suggestions.append("➔ Your CV has potential but can be improved! Align your experience with the job role more clearly.")
        suggestions.append("➔ Tailor your skillset and achievements according to the company's expectations.")
        suggestions.append("➔ Add more quantifiable achievements (numbers and stats) that reflect your impact.")
    elif score < 85:
        suggestions.append("➔ Your CV is strong, but slight improvements could be made to make it more job-specific.")
        suggestions.append("➔ Emphasize skills and experience that closely align with the job role. Highlight any leadership positions.")
        suggestions.append("➔ Focus on projects that match the job’s core requirements to make your CV more attractive.")
    else:
        suggestions.append("➔ Your CV is quite well-matched! Just polish formatting and highlight major achievements more.")
        suggestions.append("➔ If possible, tailor your CV further with specific accomplishments related to the role.")
        suggestions.append("➔ Ensure you have a concise and professional summary at the top to catch the recruiter’s attention.")

    # Always generic suggestion
    suggestions.append("➔ Keep your CV concise, focused, and job-specific. Customize for each role.")

    return suggestions
