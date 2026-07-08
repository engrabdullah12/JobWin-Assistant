import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3.1-flash-lite")

def resume_agent(resume_text):
    prompt = f"""You are an expert resume reviewer.
Analyze this resume and provide:
1. Overall strength (out of 10)
2. Key strengths
3. Weaknesses
4. Suggestions to improve
Resume: {resume_text}"""
    response = model.generate_content(prompt)
    return response.text.strip()
