import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3.1-flash-lite")

def tailor_resume(resume_text, jd_text):
Your task is to completely rewrite the candidate's resume to match the Job Description as closely as possible, while maintaining truthfulness.

CRITICAL REQUIREMENT: The final resume MUST fit perfectly on a SINGLE PAGE. Do NOT delete important details or jobs. Instead, achieve the 1-page limit by using compact styling (e.g., smaller fonts like 10pt/11px, tight line-height like 1.2, and minimal margins). 

You MUST output the final resume as valid, self-contained HTML that EXACTLY mimics a minimalist, professional template.

### Job Description:
{jd_text}

### Original Resume:
{resume_text}

### Required HTML Structure & Styling:
The HTML must use inline styles or a <style> block that achieves this exact look:
- USE FULL PAGE WIDTH! Do not restrict the width to a narrow column. Use width: 100% and max-width: 850px.
- Use a clean, sans-serif font (like Arial, Helvetica, or Inter) with a base size of 10pt or 11px to fit more content.
- Centered header containing: Name (Large, Bold, Black), Title (Medium, Blue/Purple color like #6b21a8).
- Contact info below title, centered, with icons (use simple emojis or text symbols like ✉️, 🔗, 📍).
- Section headers (SUMMARY, WORK EXPERIENCE, EDUCATION, PROJECTS, SKILLS) should be left-aligned or centered, ALL CAPS, bold, purple/blue color (#6b21a8), with a solid thin line below them.
- Work experience should be a flexbox or table: Title (Bold) & Company (Normal) on the left, and Date (Italic) aligned to the right edge.
- Use bullet points for descriptions. Make them concise and highly tailored to the JD. Use tight line-height (1.2) and no margin between bullets.
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
