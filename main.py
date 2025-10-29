from extract_text import extract_text_from_pdf, extract_text_from_docx
from ranker import weighted_resume_score

file_path = "data/sample_resume.pdf"
job_description_path = "data/job_description.txt"

with open(job_description_path, "r", encoding="utf-8") as f:
    job_desc = f.read()

text = extract_text_from_pdf(file_path) if file_path.endswith(".pdf") else extract_text_from_docx(file_path)
scores = weighted_resume_score(text, job_desc)

print("Section-wise Scores:", scores)
print(f"Overall Resume Match: {scores['final_score']}%")