import openai
import os
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_roadmap(missing_skills):
    skills_list = ", ".join(missing_skills)
    prompt = f"""
You are a career coach.
Create a 30-day learning roadmap to learn these skills: {skills_list}

Format it week by week like:
Week 1: ...
Week 2: ...
Week 3: ...
Week 4: ...

Be specific with resources and daily tasks.
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def generate_interview_questions(resume_text, jd_text):
    prompt = f"""
You are an expert interviewer.
Generate 10 interview questions based on this resume and job description.
Mix technical and behavioral questions.

Resume: {resume_text}
Job Description: {jd_text}

Return as a numbered list.
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()