import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3.1-flash-lite")

def generate_upwork_proposal(resume_text, jd_text, hiring_rate="Unknown", payment_verified=True, other_notes=""):
    prompt = f"""You are an elite Upwork Freelancer with a 100% Job Success Score and millions of dollars earned.
Your goal is to write a highly customized, high-converting Upwork proposal based on the Job Description and the candidate's Resume.

### Modern Upwork Proposal Rules (Researched):
1. **The First 2 Lines (The Hook):** Clients only see the first two lines of a proposal in their list. NEVER start with generic introductions like "Hi, my name is..." or "I am a senior developer...". Instead, start with a direct hook about their project, showing you understand their problem immediately (e.g. "I can fix your Next.js hydration error today...", or "Here is how I would approach building your custom API...").
2. **Conciseness is King:** Keep the proposal under 250 words. Busy clients scan proposals. Use bullet points for structural clarity.
3. **Relevance over Resume:** Selectively highlight only 2-3 specific accomplishments or skills from the resume that directly solve the client's biggest pain points in the JD.
4. **Call to Action (CTA):** End with a low-friction question or call to action (e.g., "Do you have a preferred API provider, or should we use OpenAI?", "Let's do a quick chat to map out the scope.").
5. **No AI Clichés:** Avoid generic corporate jargon, exclamation mark overload, and placeholders. Be conversational, direct, and professional.

### Inputs:
- **Client Hiring Rate:** {hiring_rate}
- **Payment Verified:** {"Yes" if payment_verified else "No"}
- **Other Job Notes:** {other_notes}
- **Job Description:**
{jd_text}
- **Candidate's Resume:**
{resume_text}

### Output Format (Markdown):
1. **## Client Quality Analysis** (A 1-2 sentence quick check of whether the client's metrics make them a safe and high-paying lead).
2. **## Proposal** (The actual proposal text, ready to copy-paste).
3. **## Recommended Attachments & Next Steps** (2 specific files or portfolio screenshots from the resume they should attach, plus 1 question to ask the client).
"""
    response = model.generate_content(prompt)
    return response.text.strip()
