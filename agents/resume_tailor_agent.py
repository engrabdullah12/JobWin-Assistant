import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3.1-flash-lite")

def tailor_resume(resume_text, jd_text):
    prompt = f"""You are an elite executive technical resume writer.
Your task is to completely rewrite and tailor the candidate's resume to match the Target Job Description as closely as possible, while strictly maintaining 100% truthfulness and matching the exact visual design template from the sample provided.

CRITICAL RULES:
1. STRICT TRUTHFULNESS (ZERO HALLUCINATION / NO BLUFFING):
   - Copy Education, Degrees, Universities, Company Names, Job Titles, and Dates EXACTLY and TRUTHFULLY from the Original Resume.
   - Do NOT invent fake degrees, fake universities, fake companies, or fake work dates.
   - Adapt project descriptions, bullet points, and skills to highlight relevant technical keywords from the Job Description, but ground all achievements strictly in the candidate's actual experience.

2. EXACT VISUAL & TYPOGRAPHY BLUEPRINT (MATCHING THE SAMPLE RESUME):
   - Candidate Name: ALL CAPS, Centered, 22pt font, Bold, Dark Color (#0f172a).
   - Candidate Job Title: Centered, 13pt font, Bold, Accent Color #1e40af (Royal Blue).
   - Contact Bar: Centered horizontal bar enclosed between thin top and bottom lines (`border-top: 1px solid #cbd5e1; border-bottom: 1px solid #cbd5e1; padding: 4px 0; margin: 6px 0 10px 0; flex layout with gap: 12px; font-size: 9.5pt`). Include icons or symbols for Phone, Email, LinkedIn, GitHub, Location.
   - Section Titles (SUMMARY, WORK EXPERIENCE, EDUCATION, PROJECTS, SKILLS, CERTIFICATIONS, REFERENCES): Centered, ALL CAPS, 11.5pt font, Bold, Accent Color #1e40af, with a solid 1.5px bottom border (#1e40af) and 6px bottom margin.
   - Work Experience & Project Item Headers: Flex row with `Job Title — Company Name` (Bold) on the LEFT, and `(Employment Type, Remote) MM/YYYY – Date` (Italic, 9.5pt) on the RIGHT.
   - Keywords Bolding: Automatically BOLD key technical terms (e.g., <b>Voice AI</b>, <b>RAG systems</b>, <b>LangChain</b>, <b>FastAPI</b>, <b>Python</b>) inside summary, experience, project descriptions, and skills to maximize ATS readability.
   - Skills Format: Bulleted list with bold category headers (e.g., ● <b>AI/ML:</b> LangChain, OpenAI, Pinecone...).
   - Body Font Size: Default 10.5pt to 11pt font size, line-height 1.3, tight padding to strictly fit onto 1 SINGLE A4 PAGE.

3. REQUIRED HTML STRUCTURE & CSS BLUEPRINT:
   Output self-contained HTML starting directly with `<div class="resume-container">`:
   ```html
   <div class="resume-container">
     <style>
       .resume-container {{
         font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
         color: #0f172a;
         background: #ffffff;
         width: 100%;
         max-width: 210mm;
         margin: 0 auto;
         padding: 4mm 10mm 8mm 10mm;
         box-sizing: border-box;
         font-size: 11pt;
         line-height: 1.3;
       }}
       .resume-name {{ font-size: 22pt; font-weight: 800; text-align: center; text-transform: uppercase; color: #0f172a; letter-spacing: 0.5px; margin-top: 0; padding-top: 0; margin-bottom: 2px; }}
       .resume-title {{ font-size: 13pt; font-weight: 700; text-align: center; color: #1e40af; margin-bottom: 4px; }}
       .resume-contact-bar {{
         display: flex; flex-wrap: wrap; justify-content: center; align-items: center; gap: 12px;
         font-size: 9.5pt; color: #334155; border-top: 1px solid #cbd5e1; border-bottom: 1px solid #cbd5e1;
         padding: 4px 0; margin: 6px 0 10px 0;
       }}
       .resume-section-title {{
         text-align: center; font-size: 11.5pt; font-weight: 800; text-transform: uppercase;
         color: #1e40af; letter-spacing: 0.5px; border-bottom: 1.5px solid #1e40af;
         padding-bottom: 2px; margin-top: 10px; margin-bottom: 6px;
       }}
       .resume-item-header {{ display: flex; justify-content: space-between; align-items: baseline; font-weight: bold; margin-bottom: 2px; font-size: 11pt; }}
       .resume-item-title {{ font-weight: 700; color: #0f172a; }}
       .resume-item-company {{ font-weight: 400; color: #334155; }}
       .resume-item-date {{ font-style: italic; font-weight: 400; font-size: 9.5pt; color: #475569; }}
       .resume-text {{ font-size: 10.5pt; line-height: 1.3; margin-bottom: 6px; color: #1e293b; text-align: justify; }}
       ul.resume-bullets {{ margin: 2px 0 6px 16px; padding: 0; font-size: 10.5pt; list-style-type: disc; }}
       ul.resume-bullets li {{ margin-bottom: 2px; line-height: 1.3; }}
     </style>
     <!-- Resume Content Starts Immediately Here Without Top Margin -->
   </div>
   ```

### Target Job Description:
{jd_text}

### Original Candidate Resume (Source of Truth):
{resume_text}

Return ONLY the raw HTML code starting with <div class="resume-container">. Do not include markdown codeblocks or ```html tags.
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