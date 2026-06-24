import openai
import os
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_cover_letter(resume_text, jd_text):
    prompt = f"""
You are a professional cover letter writer.
Write a compelling cover letter based on this resume and job description.

Resume:
{resume_text}

Job Description:
{jd_text}

Write a professional, personalized cover letter. Keep it under 300 words.
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()