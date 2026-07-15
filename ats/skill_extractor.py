import io
import pdfplumber
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3.1-flash-lite")

def extract_text_from_pdf(pdf_input):
    text = ""
    try:
        # Support both file path and bytes
        pdf_file = io.BytesIO(pdf_input) if isinstance(pdf_input, bytes) else pdf_input
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    except Exception as e:
        print(f"pdfplumber error: {e}")
        
    # Fallback to Gemini inline PDF parsing if pdfplumber fails or returns no content (scanned PDF)
    if len(text.strip()) < 50:
        try:
            print("pdfplumber returned insufficient text. Falling back to Gemini inline PDF parser...")
            if isinstance(pdf_input, bytes):
                pdf_bytes = pdf_input
            else:
                with open(pdf_input, "rb") as f:
                    pdf_bytes = f.read()
            
            response = model.generate_content([
                {
                    "mime_type": "application/pdf",
                    "data": pdf_bytes
                },
                "Extract all text from this resume PDF. Maintain the exact structural layout, headings, and details. Do not explain anything, just output the clean text of the resume."
            ])
            extracted_text = response.text.strip()
            if extracted_text:
                text = extracted_text
        except Exception as e:
            print(f"Gemini PDF extraction fallback error: {e}")
            
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
