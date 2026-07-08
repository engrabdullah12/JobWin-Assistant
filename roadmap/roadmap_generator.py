import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3.1-flash-lite")

def generate_roadmap(missing_skills):
    skills_list = ", ".join(missing_skills)
    prompt = f"""You are a career coach.
Create a 30-day learning roadmap to learn: {skills_list}
Format week by week:
Week 1: ...
Week 2: ...
Week 3: ...
Week 4: ..."""
    response = model.generate_content(prompt)
    return response.text.strip()

def generate_interview_questions(resume_text, jd_text):
    prompt = f"""You are an expert interviewer.
Generate 10 interview questions based on this resume and job description.
Mix technical and behavioral questions.
Resume: {resume_text}
Job Description: {jd_text}
Return as a numbered list."""
    response = model.generate_content(prompt)
    return response.text.strip()
