import streamlit as st
import os
import json
from utils.extract_text import extract_text_from_pdf
from utils.match_score import calculate_match, suggest_improvements

# Load job descriptions
with open('jobs/job_description.json', 'r') as f:
    job_descriptions = json.load(f)

st.set_page_config(page_title="CV Matcher App", page_icon="📄", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #f2f2f2, #ffffff);
        font-family: 'Arial', sans-serif;
    }

    .title {
        color: #4CAF50;
        font-size: 36px;
        font-weight: bold;
    }

    .upload-box {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }

    .btn-match {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s;
    }

    .btn-match:hover {
        background-color: #45a049;
    }

    .cv-box {
        background-color: #fafafa;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.05);
        max-height: 600px;
        overflow-y: scroll;
    }

    .score-card {
        background-color: #eeeeee;
        padding: 15px;
        border-radius: 8px;
        margin-top: 20px;
    }

    .suggestions {
        margin-top: 20px;
    }

    </style>
""", unsafe_allow_html=True)

st.title("📄 CV Matcher App", anchor="title")

# Upload CV
cv_file = st.file_uploader("Upload your CV (PDF only)", type=["pdf"], key="cv")

if cv_file:
    upload_path = os.path.join('uploads', cv_file.name)
    with open(upload_path, "wb") as f:
        f.write(cv_file.getbuffer())
    st.success("CV uploaded successfully!")

    # Choose Job Role
    selected_job = st.selectbox("Select your target job role", list(job_descriptions.keys()))

    if selected_job:
        job_info = job_descriptions[selected_job]
        job_description = job_info['description'] + " Skills Required: " + ", ".join(job_info['skills_required'])

        # Layout for Extracted Text and Match Score
        col1, col2 = st.columns([1, 3])  # Adjust column width for better layout

        with col1:
            st.subheader("📄 Extracted CV Text")
            cv_text = extract_text_from_pdf(upload_path)
            st.text_area("Extracted Text", value=cv_text, height=300, key="extracted_text", disabled=True)

        with col2:
            st.subheader("🚀 Match Your CV with Job Description")
            if st.button("Match Now 🚀", key="match_button"):
                match_percentage = calculate_match(cv_text, job_description)
                st.subheader(f"📈 ATS Match Score: {match_percentage}%")

                if match_percentage >= 80:
                    st.success("Great! Your CV is a strong match! 🎯")
                elif match_percentage >= 50:
                    st.warning("Good, but can be improved! 🛠️")
                else:
                    st.error("Weak match. Consider improving your CV! 🚨")

                # Suggestions (Optional)
                st.subheader("📝 Suggestions to Improve Your CV")
                suggestions = suggest_improvements(cv_text, job_description, match_percentage)
                for suggestion in suggestions:
                    st.info(suggestion)

