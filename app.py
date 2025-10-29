import streamlit as st
from extract_text import extract_text_from_pdf, extract_text_from_docx
from resume_parser import extract_entities
from ranker import weighted_resume_score
from batch_ranker import batch_rank_resumes
import zipfile, os
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="AI Resume Ranker SaaS",
    layout="wide",
    page_icon="📝"
)

# --- SIDEBAR ---
st.sidebar.title("Job Description & Settings")

job_description = st.sidebar.text_area("Paste Job Description Here", height=250)

weights_skills = st.sidebar.slider("Skills Weight", 0.0, 1.0, 0.5)
weights_exp = st.sidebar.slider("Experience Weight", 0.0, 1.0, 0.3)
weights_edu = st.sidebar.slider("Education Weight", 0.0, 1.0, 0.2)

weights = {"skills": weights_skills, "experience": weights_exp, "education": weights_edu}

st.sidebar.markdown("---")
st.sidebar.info("Adjust the weights for Skills, Experience, and Education to change ranking priorities.")

# --- TABS ---
tab1, tab2 = st.tabs(["Single Resume", "Batch Resume"])

# --- SINGLE RESUME TAB ---
with tab1:
    st.header("📋 Single Resume Ranking")
    uploaded_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"], key="single")

    if uploaded_file and job_description.strip():
        # Save file temporarily
        file_name = uploaded_file.name
        with open(file_name, "wb") as f:
            f.write(uploaded_file.read())

        # Extract text
        if file_name.endswith(".pdf"):
            text = extract_text_from_pdf(file_name)
        else:
            text = extract_text_from_docx(file_name)

        # Extract entities
        details = extract_entities(text)
        st.subheader("📄 Extracted Resume Info")
        st.json(details)

        # Compute weighted score
        scores = weighted_resume_score(text, job_description, weights)
        st.subheader("🏆 Section-wise Scores")

        st.progress(int(scores['skills_similarity']))
        st.caption(f"Skills Match: {scores['skills_similarity']}%")

        st.progress(int(scores['experience_similarity']))
        st.caption(f"Experience Match: {scores['experience_similarity']}%")

        st.progress(int(scores['education_similarity']))
        st.caption(f"Education Match: {scores['education_similarity']}%")

        st.subheader("🎯 Overall Score")
        st.metric("Resume Match", f"{scores['final_score']}%")

# --- BATCH RESUME TAB ---
with tab2:
    st.header("📂 Batch Resume Ranking")
    uploaded_zip = st.file_uploader("Upload Resumes ZIP", type=["zip"], key="batch")

    if uploaded_zip and job_description.strip():
        os.makedirs("data/resumes", exist_ok=True)
        zip_path = "data/resumes.zip"
        with open(zip_path, "wb") as f:
            f.write(uploaded_zip.read())

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall("data/resumes")

        # Save job description temporarily
        with open("data/job_description.txt", "w", encoding="utf-8") as f:
            f.write(job_description)

        with st.spinner("Ranking resumes..."):
            df = batch_rank_resumes("data/resumes", "data/job_description.txt", "output/ranked_resumes.csv")

        st.success("✅ Batch ranking complete!")

        # Styled leaderboard
        st.subheader("🏆 Top Ranked Resumes")
        st.dataframe(df.style.background_gradient(subset=['Overall Score'], cmap='YlGnBu'))

        # CSV download
        csv_data = df.to_csv(index=False)
        st.download_button(
            label="Download Ranked Resumes",
            data=csv_data,
            file_name="ranked_resumes.csv",
            mime="text/csv"
        )