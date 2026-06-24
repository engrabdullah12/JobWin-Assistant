import openai
import os
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def resume_agent(resume_text):
    prompt = f"""
You are an expert resume reviewer.
Analyze this resume and provide:
1. Overall strength (out of 10)
2. Key strengths
3. Weaknesses
4. Suggestions to improve

Resume:
{resume_text}
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()