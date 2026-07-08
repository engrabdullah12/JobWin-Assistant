import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3.1-flash-lite")

def tailor_resume(resume_text, jd_text):
    prompt = f"""You are an expert technical resume writer.
Your task is to completely rewrite the candidate's resume to match the Job Description as closely as possible, while maintaining truthfulness (don't invent jobs they didn't do, but highlight relevant aspects).

CRITICAL REQUIREMENT: The final resume MUST fit perfectly on a SINGLE PAGE. Condense descriptions, remove fluffy older jobs, and use concise, hard-hitting bullet points. Do not exceed 1 page of content.

You MUST output the final resume as valid, self-contained HTML that EXACTLY mimics the design provided in the sample (a minimalist, professional template with centered header, lines separating sections, and clean typography).

### Job Description:
{jd_text}

### Original Resume:
{resume_text}

### Required HTML Structure & Styling:
The HTML must use inline styles or a <style> block that achieves this exact look:
- Clean, sans-serif font (like Arial or Inter).
- Centered header containing: Name (Large, Bold, Black), Title (Medium, Blue/Purple color like #6b21a8).
- Contact info below title, centered, with icons (use simple emojis or text symbols like ✉️, 🔗, 📍).
- Section headers (SUMMARY, WORK EXPERIENCE, EDUCATION, PROJECTS, SKILLS) should be centered, ALL CAPS, bold, purple/blue color (#6b21a8), with a solid thin line below them.
- Work experience should have: Title (Bold) — Company (Normal) on the left, and Date (Italic) on the right.
- Use bullet points for descriptions. Make them concise and highly tailored to the JD.
- No markdown formatting wrappers (like ```html), JUST output the raw HTML code starting with <div class="resume-container"> or similar. Make sure the background is white and text is black.

Return ONLY the raw HTML code. Do not include any explanation.
"""
    response = model.generate_content(prompt)
    html_content = response.text.strip()
    
    # Strip markdown if model includes it
    if html_content.startswith("```html"):
        html_content = html_content[7:]
    if html_content.startswith("```"):
        html_content = html_content[3:]
    if html_content.endswith("```"):
        html_content = html_content[:-3]
        
    return html_content.strip()
