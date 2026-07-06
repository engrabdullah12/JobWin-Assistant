content = """# 🤖 AI Recruitment Copilot

> An AI-powered end-to-end recruitment assistant that helps job seekers optimize their job applications, calculate ATS scores, generate cover letters, prepare for interviews, and automate cold email outreach to HRs.

---

## 📌 Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [ML Models Used](#ml-models-used)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [How to Run](#how-to-run)
- [How ATS Score is Calculated](#how-ats-score-is-calculated)
- [Cold Email Sender Setup](#cold-email-sender-setup)
- [Environment Variables](#environment-variables)
- [Troubleshooting](#troubleshooting)
- [Author](#author)

---

## 📖 About the Project

As a 2026 fresher actively applying for jobs, I noticed that most resumes never reach a human recruiter — they get filtered out by **ATS (Applicant Tracking System)** software automatically.

So I built this tool to fight that problem.

**AI Recruitment Copilot** analyzes your resume against any job description and gives you a detailed report — what is matching, what is missing, and exactly what to do next.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📊 ATS Score Calculator | Calculates match score using Keywords, Semantic Similarity, Experience, Education and Format Check |
| 🔍 Skill Gap Analysis | Finds missing skills between your resume and job description |
| 📄 Resume Analysis | AI-powered detailed resume review with improvement suggestions |
| ✉️ Cover Letter Generator | Generates personalized cover letter based on resume and JD |
| ❓ Interview Questions | Generates 10 relevant technical and behavioral questions |
| 🗺️ Learning Roadmap | Creates 30-day learning plan for missing skills |
| 📧 Cold Email Sender | Sends bulk personalized emails with resume to multiple HRs automatically |
| 💬 AI Career Chatbot | Career guidance chatbot powered by RAG architecture |

---

## 🛠️ Tech Stack

| Category | Tools |
|---|---|
| Language | Python |
| Frontend | Streamlit |
| LLM | LLaMA 3.3 70B via Groq API (Free) |
| Embedding Model | all-MiniLM-L6-v2 (Sentence Transformers) |
| Vector Database | Qdrant (In-Memory) |
| PDF Parsing | pdfplumber |
| API Backend | FastAPI |
| Email Sending | smtplib (Gmail SMTP) |
| Excel Reading | pandas |
| Environment | python-dotenv |
| Version Control | Git + GitHub |

---

## 🤖 ML Models Used

| Model | Provider | Purpose |
|---|---|---|
| LLaMA 3.3 70B | Meta (via Groq) | Skill extraction, cover letter, interview questions, roadmap, chatbot |
| all-MiniLM-L6-v2 | Microsoft | Semantic similarity scoring, text embeddings for RAG |

---

## 📁 Project Structure

AI-Recruitment-Copilot/
│
├── agents/
│   ├── init.py
│   ├── ats_agent.py
│   ├── career_agent.py
│   ├── interview_agent.py
│   ├── resume_agent.py
│   └── router_agent.py
│
├── ats/
│   ├── init.py
│   ├── ats_score.py
│   └── skill_extractor.py
│
├── cold_email/
│   ├── init.py
│   └── sender.py
│
├── cover_letter/
│   ├── init.py
│   └── generator.py
│
├── data/
│   ├── knowledge_base/
│   └── uploads/
│
├── rag/
│   ├── init.py
│   ├── embeddings.py
│   ├── qdrant_store.py
│   └── retriever.py
│
├── roadmap/
│   ├── init.py
│   └── roadmap_generator.py
│
├── streamlit_app/
│   ├── init.py
│   └── app.py
│
├── workflows/
├── .env
├── .gitignore
├── README.md
└── requirements.txt

---

## ⚙️ Setup Instructions

### Step 1 — Clone the Repository

```bash
git clone https://github.com/NehaBharti16/AI-Recruitment-Copilot.git
```

### Step 2 — Go to Project Folder

**Windows:**
```bash
cd AI-Recruitment-Copilot
```

If cloned to a specific location:
```bash
cd C:\\Users\\YourName\\Downloads\\AI-Recruitment-Copilot
```

**Mac/Linux:**
```bash
cd AI-Recruitment-Copilot
```

### Step 3 — Install All Dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Get Free Groq API Key

1. Go to https://console.groq.com
2. Sign up for free
3. Go to API Keys and create a new key
4. Copy the key

### Step 5 — Create .env File

Create a file called .env in the root project folder and paste this:

GROQ_API_KEY=your-groq-api-key-here
QDRANT_HOST=localhost
QDRANT_PORT=6333

Replace your-groq-api-key-here with your actual Groq API key

---

## ▶️ How to Run

### Run the App

```bash
python -m streamlit run streamlit_app/app.py
```

### Open in Browser

App will automatically open at:

http://localhost:8501

If it does not open automatically — copy this URL and paste in your browser.

---

## 📊 How ATS Score is Calculated

Unlike simple keyword matchers, this tool uses 5 different scoring methods:

Final ATS Score =
Keyword Match Score   x 30%   (skills from JD vs resume)

Semantic Score        x 30%   (meaning-based similarity using AI)
Experience Score      x 20%   (years required vs years you have)
Education Score       x 10%   (qualification match)
Format Score          x 10%   (resume ATS-friendliness check)

This gives a much more accurate and realistic ATS score compared to simple keyword matching tools.

---

## 📧 Cold Email Sender Setup

This feature sends personalized bulk emails with your resume attached to multiple HRs automatically.

### Step 1 — Enable Gmail 2-Step Verification

1. Go to https://myaccount.google.com/security
2. Enable 2-Step Verification

### Step 2 — Generate Gmail App Password

1. Go directly to https://myaccount.google.com/apppasswords
2. Type any name like recruitment
3. Click Create
4. Copy the 16-digit password and remove all spaces
5. Paste in App Password field in the app

### Step 3 — Prepare Your Excel File

Create an Excel file with exactly these columns:

| S.No | Company Name | HR / Contact Person | Email ID |
|---|---|---|---|
| 1 | Google | John Smith | john@google.com |
| 2 | Microsoft | HR Team | hr@microsoft.com |

### Step 4 — Use in App

1. Go to Cold Email Sender page
2. Enter your Gmail address
3. Enter your App Password
4. Upload the Excel file
5. Preview the email content
6. Set delay between emails (recommended 30 seconds)
7. Click Send Emails


Note: App Password is different from your regular Gmail password.
It is a 16-digit code generated specifically for this app.
Without App Password the email sending will fail.

---

## 🔑 Environment Variables

| Variable | Description | Required |
|---|---|---|
| GROQ_API_KEY | Free API key from console.groq.com | Yes |
| QDRANT_HOST | Qdrant host — keep as localhost | Yes |
| QDRANT_PORT | Qdrant port — keep as 6333 | Yes |
| SENDER_EMAIL | Your Gmail for cold emails | Optional |
| SENDER_PASSWORD | Gmail App Password | Optional |

---

## 🔧 Troubleshooting

| Problem | Solution |
|---|---|
| streamlit not recognized | Use python -m streamlit run streamlit_app/app.py |
| ModuleNotFoundError | Run pip install -r requirements.txt |
| GROQ_API_KEY missing | Check .env file has correct key |
| GroqError missing credentials | Make sure .env file is in root project folder |
| App opens but shows error | Make sure you are inside correct project folder |
| 0 valid HR emails found | Check Excel column names match exactly |
| SMTPAuthenticationError | Use Gmail App Password not regular password |
| Cold email not sending | Enable 2-Step Verification and regenerate App Password |

---

## ⚠️ Important Notes

- Never commit your .env file — it contains your API keys
- Groq API is completely free for personal use
- Qdrant runs in-memory — data resets when app restarts
- Cold Email requires Gmail App Password — not your regular Gmail password
- Set 30 second delay between emails to avoid Gmail spam filters
- Keep resume PDF size under 5MB for best results

---

## 🙋 Author

**Neha Bharti**

- GitHub: https://github.com/NehaBharti16
- LinkedIn: https://linkedin.com/in/neha-bharti-61956b348
- Email: nehab3099@gmail.com

---

## ⭐ Support

If this project helped you — please give it a star on GitHub!

Share it with fellow freshers who are struggling with job applications!

---

Built with love by Neha Bharti — a fresher who got tired of getting ignored and decided to build something about it.
""" 

with open("README.md", "w", encoding="utf-8") as f:
    f.write(content)

print("README.md created successfully!")

<!-- # 🤖 AI Recruitment Copilot

An AI-powered system to help job seekers improve their chances of getting selected.

## Features
- ATS Score Calculator
- Skill Gap Analysis
- Cover Letter Generator
- Interview Question Generator
- Learning Roadmap Generator
- AI Career Chatbot with RAG

## Tech Stack
- Python, Streamlit
- Groq API (LLaMA 3.3)
- Qdrant Vector DB
- LangChain, Sentence Transformers
- pdfplumber

## Setup
1. Clone the repo
2. Install requirements: `pip install -r requirements.txt`
3. Add your Groq API key to `.env`
4. Run: `python -m streamlit run streamlit_app/app.py`

## To Run
cd D:\Ai-Recruitment-Copilot\AI-Recruitment-Copilot
python -m streamlit run streamlit_app/app.py -->