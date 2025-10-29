import os
import pandas as pd
from extract_text import extract_text_from_pdf, extract_text_from_docx
from ranker import weighted_resume_score

def batch_rank_resumes(resume_folder, job_description_path, output_csv="output/ranked_resumes.csv"):
    with open(job_description_path, "r", encoding="utf-8") as f:
        job_desc = f.read()

    leaderboard = []

    for file_name in os.listdir(resume_folder):
        if not file_name.lower().endswith((".pdf", ".docx")):
            continue
        file_path = os.path.join(resume_folder, file_name)
        text = extract_text_from_pdf(file_path) if file_name.endswith(".pdf") else extract_text_from_docx(file_path)
        scores = weighted_resume_score(text, job_desc)
        leaderboard.append({
            "Resume": file_name,
            "Skills Match": scores["skills_similarity"],
            "Experience Match": scores["experience_similarity"],
            "Education Match": scores["education_similarity"],
            "Overall Score": scores["final_score"]
        })

    df = pd.DataFrame(leaderboard)
    df.sort_values(by="Overall Score", ascending=False, inplace=True)
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df.to_csv(output_csv, index=False)
    print(f"✅ Batch ranking complete. Results saved to {output_csv}")
    return df

if __name__ == "__main__":
    df = batch_rank_resumes("data/resumes", "data/job_description.txt")
    print(df.head(10))