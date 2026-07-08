import pdfplumber
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3.1-flash-lite")

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_skills(text, source="resume"):
    prompt = f"""You are an expert HR analyst.
Extract all technical skills from this {source} text.
Return ONLY a Python list like: ['Python', 'SQL', 'Docker']
No explanation. Just the list.

Text:
{text}"""
    response = model.generate_content(prompt)
    raw = response.text.strip()
    # Handle possible markdown formatting
    if raw.startswith("```"):
        raw = "\n".join(raw.split("\n")[1:-1]).strip()
    try:
        skills = eval(raw)
    except Exception:
        skills = []
    return skills
