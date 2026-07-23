import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3.1-flash-lite")

def tailor_resume(resume_text, jd_text):
    prompt = f"""You are an elite technical resume writer.
Your task is to rewrite and tailor the candidate's resume to match the Target Job Description as closely as possible, while strictly maintaining 100% truthfulness and fitting onto EXACTLY ONE SINGLE A4 PAGE.

CRITICAL RULES:
1. STRICT TRUTHFULNESS (ZERO HALLUCINATION / NO BLUFFING):
   - Copy Education, Degrees, Universities, Company Names, Job Titles, and Dates EXACTLY and TRUTHFULLY from the Original Resume.
   - Do NOT invent fake degrees, fake universities, fake companies, or fake work dates.
   - Tailor the bullet points, projects, and skills to highlight relevant technical keywords from the Job Description, but ground all achievements strictly in the candidate's actual experience.

2. STRICT 1-PAGE TYPOGRAPHY & LAYOUT CONSTRAINTS:
   - Candidate Name Header: Large font (20pt / 1.5rem), Bold, Dark Color (#0f172a), Centered.
   - Candidate Subtitle / Professional Title: Medium font (13pt / 1rem), Bold, Color #2563eb (Blue), Centered.
   - Contact Bar: Compact 9.5pt font, Centered below title (e.g., Email | Phone | Location | LinkedIn).
   - ALL BODY TEXT, SUMMARY, BULLET POINTS, SKILLS, EDUCATION & PROJECTS MUST USE EXACTLY DEFAULT 11pt FONT (14px) WITH A COMPACT LINE-HEIGHT OF 1.25.
   - Section Titles (SUMMARY, WORK EXPERIENCE, PROJECTS, SKILLS, EDUCATION): Left-aligned or Centered, ALL CAPS, Bold, 11pt, Color #1e40af, with a solid 1px bottom border (#e2e8f0) and 6px bottom margin.
   - TIGHT SPACING: Use minimal margins/padding (6px-8px between sections, 2px between bullet points) to GUARANTEE everything fits on 1 single A4 page.
   - Keep bullet points to max 2-3 high-impact, punchy points per role/project.

3. REQUIRED HTML/CSS BLUEPRINT:
   - Output valid, self-contained HTML starting directly with `<div class="resume-container">`.
   - Include an embedded `<style>` block ensuring:
     ```css
     .resume-container {{
       font-family: 'Inter', Arial, sans-serif;
       color: #0f172a;
       background: #ffffff;
       width: 100%;
       max-width: 210mm;
       margin: 0 auto;
       padding: 8mm 10mm;
       box-sizing: border-box;
       font-size: 11pt;
       line-height: 1.25;
     }}
     .resume-header {{ text-align: center; margin-bottom: 10px; }}
     .resume-name {{ font-size: 20pt; font-weight: 800; color: #0f172a; margin-bottom: 2px; }}
     .resume-subtitle {{ font-size: 13pt; font-weight: 700; color: #2563eb; margin-bottom: 4px; }}
     .resume-contact {{ font-size: 9.5pt; color: #475569; }}
     .resume-section-title {{ font-size: 11pt; font-weight: 700; text-transform: uppercase; color: #1e40af; border-bottom: 1px solid #cbd5e1; padding-bottom: 2px; margin-top: 10px; margin-bottom: 6px; }}
     .resume-content {{ font-size: 11pt; line-height: 1.25; margin-bottom: 4px; }}
     ul.resume-bullets {{ margin: 2px 0 6px 18px; padding: 0; font-size: 11pt; }}
     ul.resume-bullets li {{ margin-bottom: 2px; font-size: 11pt; line-height: 1.25; }}
     ```

### Target Job Description:
{jd_text}

### Original Candidate Resume (Source of Truth):
{resume_text}

Return ONLY the raw HTML code without markdown codeblocks. Do not include introductory notes or ```html tags.
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