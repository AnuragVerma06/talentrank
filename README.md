# 🧠 AI Resume Ranker

AI Resume Ranker is a smart tool that analyzes multiple resumes against a given job description and ranks them based on skill relevance.  
Built with **Python + Streamlit + spaCy**, it’s perfect for recruiters, startups, and HR teams.

---

## 🌟 Features

✅ Upload multiple resumes (`.pdf` or `.docx`)  
✅ Paste or upload job descriptions  
✅ AI skill extraction using spaCy NLP  
✅ Automatic candidate ranking  
✅ Download ranked results as `.csv`  
✅ SaaS-ready Streamlit web UI  

---

## 🛠️ Installation

```bash
git clone https://github.com/<your-username>/talentrank.git
cd talentrank
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

---

## ▶️ Run the App Locally

```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## ☁️ Deploy on Streamlit Cloud (Free)

1. Go to [https://share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub repo
3. Select your repo and branch (`main`)
4. Set `app.py` as the main file
5. Deploy 🚀

Your app will be live at:

```
https://<your-username>-talentrank.streamlit.app
```

---

## 📁 Project Structure

```
talentrank/
│
├── app.py
├── extract_text.py
├── resume_parser.py
├── ranker.py
├── batch_ranker.py
│
├── data/
│   ├── job_description.txt
│   └── resumes/
│
├── output/
├── requirements.txt
├── .gitignore
├── README.md
└── .streamlit/
    └── config.toml
```

---

## 🧠 Tech Stack

- **Python 3.10+**
- **Streamlit** for UI
- **spaCy** for NLP skill extraction
- **pandas** for ranking logic
- **pdfplumber / python-docx** for text extraction

---

## 💡 Future Enhancements

- Resume parsing via AI embeddings  
- Auto-detection of resume sections  
- Custom scoring algorithm  
- Cloud storage integration  

---

## 🧑‍💻 Author

Built with ❤️ by Anurag Verma  
Feedback welcome — PRs are open!
