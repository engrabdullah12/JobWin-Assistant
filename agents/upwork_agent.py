import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3.1-flash-lite")

def generate_upwork_proposal(resume_text, jd_text, hiring_rate="Unknown", payment_verified=True, other_notes=""):
    prompt = f"""You are an expert Upwork freelancer with a 100% Job Success Score. 
Your goal is to write a highly converting, professional, and personalized Upwork proposal based on the provided Job Description and the candidate's Resume.

### Job Context:
- **Hiring Rate of Client:** {hiring_rate}
- **Payment Verified:** {"Yes" if payment_verified else "No"}
- **Other Job Notes:** {other_notes}

### Job Description:
{jd_text}

### Candidate's Resume:
{resume_text}

### Instructions:
1. **The Proposal:** Write a concise, engaging proposal. Start with a hook, show how the candidate's skills (from the resume) directly solve the client's problems (from the JD), and end with a strong call to action. Keep it under 300 words. Do not use generic greetings like "Dear Hiring Manager", try to be conversational and direct.
2. **Analysis & Strategy (Internal):** Briefly analyze if this is a good client to apply to based on the Hiring Rate and Payment Verified status.
3. **Suggested Attachments:** Provide a bulleted list of 2-3 specific portfolio items or documents the candidate should attach to this proposal to maximize their chances.

Return the response clearly formatted in Markdown with headings for 'Proposal', 'Client Analysis', and 'Suggested Attachments'.
"""
    response = model.generate_content(prompt)
    return response.text.strip()
