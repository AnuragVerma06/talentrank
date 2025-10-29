from sentence_transformers import SentenceTransformer, util
import re

model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_section(text, section_name):
    pattern = rf"(?i){section_name}[:\n](.*?)(?=\n[A-Z][A-Za-z ]{{2,}}:|\Z)"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1).strip() if match else ""

def get_similarity(text1, text2):
    emb = model.encode([text1, text2])
    return util.cos_sim(emb[0], emb[1]).item()

def weighted_resume_score(resume_text, job_description, weights=None):
    if weights is None:
        weights = {"skills": 0.5, "experience": 0.3, "education": 0.2}

    skills = extract_section(resume_text, "Skills") or resume_text
    experience = extract_section(resume_text, "Experience") or resume_text
    education = extract_section(resume_text, "Education") or resume_text

    skills_sim = get_similarity(skills, job_description)
    exp_sim = get_similarity(experience, job_description)
    edu_sim = get_similarity(education, job_description)

    final_score = (
        weights["skills"] * skills_sim +
        weights["experience"] * exp_sim +
        weights["education"] * edu_sim
    ) * 100

    return {
        "skills_similarity": round(skills_sim * 100, 2),
        "experience_similarity": round(exp_sim * 100, 2),
        "education_similarity": round(edu_sim * 100, 2),
        "final_score": round(final_score, 2)
    }