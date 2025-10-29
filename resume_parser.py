import spacy
import os
import tempfile
import re

nlp = spacy.load("en_core_web_sm")

def extract_entities(text):
    doc = nlp(text)
    entities = {"NAME": None, "EMAIL": None, "PHONE": None, "SKILLS": []}

    # Name
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            entities["NAME"] = ent.text
            break

    # Email
    email = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    if email:
        entities["EMAIL"] = email.group(0)

    # Phone
    phone = re.search(r"(\+?\d{1,3}[-\s]?)?\d{10}", text)
    if phone:
        entities["PHONE"] = phone.group(0)

    # Skills
    skills_list = [
        "python", "java", "c++", "javascript", "react", "node",
        "sql", "mongodb", "excel", "machine learning", "deep learning",
        "html", "css", "git", "aws", "django", "flask"
    ]
    found_skills = [skill.capitalize() for skill in skills_list if re.search(rf"\b{skill}\b", text.lower())]
    entities["SKILLS"] = found_skills

    return entities