import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3.1-flash-lite")

def tailor_resume(resume_text, jd_text):
    prompt = f"""You are an expert technical resume writer.
Your task is to tailor the candidate's resume to match the Job Description as closely as possible, while maintaining strict truthfulness. 

CRITICAL REQUIREMENT 1 (Preserve Content): You MUST retain ALL work experience entries, companies, job titles, education, and projects from the original resume. DO NOT delete, omit, or summarize multiple jobs/projects into a single entry to save space. Every single role and project from the original resume must appear in the tailored HTML output.

CRITICAL REQUIREMENT 2 (Format & Spacing): The entire resume must fit on exactly ONE page. To achieve this, DO NOT delete content. Instead, save space by writing highly concise bullet points (2-3 bullets per role, focused on JD relevance) and adjusting the CSS layout (compact line-height, tight margins, small padding, and clean layout).

### Job Description:
{jd_text}

### Original Resume:
{resume_text}

### Required HTML Structure & Styling:
The HTML must use inline styles or a <style> block that achieves this exact look:
- Clean, sans-serif font (like Arial or Inter, body size 10px to 11px, line-height 1.25 to 1.3).
- Centered header containing: Name (Large, Bold, Black), Title (Medium, Blue/Purple color like #6b21a8).
- Contact info below title, centered, with icons (use simple emojis or text symbols like ✉️, 🔗, 📍).
- Section headers (SUMMARY, WORK EXPERIENCE, EDUCATION, PROJECTS, SKILLS) should be centered, ALL CAPS, bold, purple/blue color (#6b21a8), with a solid thin line below them. Keep section margins very tight (margin-top: 8px, margin-bottom: 4px).
- Work experience should have: Title (Bold) — Company (Normal) on the left, and Date (Italic) on the right.
- Bullet points must be concise, bullet margins should be tight, and spacing between separate jobs/projects should be minimal (e.g. margin-bottom: 6px).
- Container padding should be compact (e.g. 15px to 20px all around) to maximize printable height.
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
