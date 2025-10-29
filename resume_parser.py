import spacy
from spacy.language import Language
from spacy.pipeline import EntityRuler

# Create a lightweight blank English model
nlp = spacy.blank("en")

# Add an EntityRuler for simple rule-based extraction
ruler = nlp.add_pipe("entity_ruler")
patterns = [
    {"label": "EMAIL", "pattern": [{"LIKE_EMAIL": True}]},
    {"label": "PHONE", "pattern": [{"TEXT": {"REGEX": r"(\+?\d{1,3}[-.\s]?)?\d{10}"}}]},
    {"label": "NAME", "pattern": [{"IS_TITLE": True}, {"IS_TITLE": True}]},
    {"label": "SKILL", "pattern": [{"LOWER": {"IN": ["python", "javascript", "react", "node", "java", "c++"]}}]},
]
ruler.add_patterns(patterns)

def extract_entities(text):
    doc = nlp(text)
    extracted = {"email": None, "phone": None, "name": None, "skills": []}

    for ent in doc.ents:
        if ent.label_ == "EMAIL":
            extracted["email"] = ent.text
        elif ent.label_ == "PHONE":
            extracted["phone"] = ent.text
        elif ent.label_ == "NAME" and extracted["name"] is None:
            extracted["name"] = ent.text
        elif ent.label_ == "SKILL":
            extracted["skills"].append(ent.text)

    return extracted