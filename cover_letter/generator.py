import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3.1-flash-lite")

import re

DEFAULT_CONTACT_INFO = """Muhammad Abdullah
Phone: +923027435603
Email: engr.abdullah1212@gmail.com
LinkedIn: www.linkedin.com/in/engr-m-abdullah-27b620333"""

def clean_cover_letter(text):
    # Remove markdown bolding and italics asterisks
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    # Remove horizontal rule lines like *** or ---
    text = re.sub(r'^\s*[\*\-_]{3,}\s*$', '', text, flags=re.MULTILINE)
    # Remove preamble lines if any
    text = re.sub(r'^(Here is|To provide|I have drafted|Below is|Draft:).*?\n\n', '', text, flags=re.IGNORECASE | re.DOTALL)
    return text.strip()

def generate_cover_letter(resume_text, jd_text):
    user_info = DEFAULT_CONTACT_INFO

    if resume_text and resume_text.strip():
        resume_context = f"Candidate Resume:\n{resume_text}\n"
    else:
        resume_context = "Candidate Resume: Not provided. Write a strong, tailored cover letter emphasizing expertise in AI Engineering, Data Science, and modern tech stack based on the job requirements.\n"

    prompt = f"""You are an elite executive cover letter writer.
Write a fully optimized, highly persuasive professional cover letter for the candidate based on the job description below.

STRICT FORMATTING AND CONTENT RULES:
1. Candidate Contact Information (Always include this exact header at the top):
{user_info}

2. NO MARKDOWN: Do NOT use asterisks (** or *), hashes (#), bullet points with asterisks, or any markdown formatting. Output plain formatted text ONLY.
3. NO PLACEHOLDERS: Do NOT use bracketed placeholders like [Company Name], [Hiring Manager], [Date], [Your Name], [Number] years. Automatically extract or infer the Job Title and Company Name from the Job Description. If company name is not mentioned, address to "Dear Hiring Team,".
4. NO INTRO CHATTER: Do NOT include any intro notes like "Here is your cover letter" or "I have drafted...". Start directly with candidate contact header, date, recipient greeting, and letter content.
5. PERSUASIVE & OPTIMIZED: Craft a compelling narrative demonstrating strong alignment with the job requirements. Keep it professional, punchy, and under 350 words.

{resume_context}
Job Application / Description:
{jd_text}
"""

    response = model.generate_content(prompt)
    raw_text = response.text.strip()
    return clean_cover_letter(raw_text)

