import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3.1-flash-lite")

def generate_cover_letter(resume_text, jd_text):
    if resume_text and resume_text.strip():
        prompt = f"""You are a professional cover letter writer.
Write a compelling cover letter based on this resume and job description.
Resume: {resume_text}
Job Description: {jd_text}
Write a professional cover letter under 300 words."""
    else:
        prompt = f"""You are a professional cover letter writer.
Write a compelling, professional cover letter based on this job description / job application.
Since no specific resume was provided, write a targeted cover letter highlighting relevant competencies, achievements, and enthusiasm for the position described in the job description.
Job Description: {jd_text}
Write a professional cover letter under 300 words."""

    response = model.generate_content(prompt)
    return response.text.strip()
