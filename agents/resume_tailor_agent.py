import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3.1-flash-lite")

def tailor_resume(resume_text, jd_text):
    prompt = f"""You are an expert technical resume writer.
Your task is to completely rewrite the candidate's resume to match the Job Description as closely as possible, while maintaining truthfulness.

CRITICAL REQUIREMENT: The final resume MUST fit perfectly on a SINGLE A4 PAGE. Do NOT delete important details or jobs. Use concise bullet points to fit the space.

You MUST output the final resume as valid, self-contained HTML using EXACTLY this structure and styling. Do NOT add custom CSS or change the layout structure:

<div style="font-family: Arial, Helvetica, sans-serif; width: 100%; max-width: 800px; margin: 0 auto; color: #000; font-size: 11px; line-height: 1.4;">
  <div style="text-align: center; margin-bottom: 12px;">
    <h1 style="font-size: 24px; margin: 0; text-transform: uppercase; font-weight: bold;">[NAME]</h1>
    <h2 style="font-size: 14px; margin: 4px 0; color: #6b21a8; font-weight: bold;">[TITLE]</h2>
    <p style="margin: 0; font-size: 11px;">[Location] | [Email] | [Phone] | [Links]</p>
  </div>
  
  <h3 style="font-size: 12px; color: #6b21a8; border-bottom: 1px solid #6b21a8; margin: 12px 0 6px 0; text-transform: uppercase; font-weight: bold;">Summary</h3>
  <p style="margin: 0; text-align: justify;">[Tailored Summary Text]</p>

  <h3 style="font-size: 12px; color: #6b21a8; border-bottom: 1px solid #6b21a8; margin: 12px 0 6px 0; text-transform: uppercase; font-weight: bold;">Technical Skills</h3>
  <p style="margin: 0;"><b>Languages:</b> [Skills]<br><b>Frameworks & Tools:</b> [Skills]</p>

  <h3 style="font-size: 12px; color: #6b21a8; border-bottom: 1px solid #6b21a8; margin: 12px 0 6px 0; text-transform: uppercase; font-weight: bold;">Professional Experience</h3>
  
  <!-- Repeat for each job -->
  <div style="margin-bottom: 10px;">
    <div style="display: flex; justify-content: space-between; align-items: baseline;">
      <div style="font-weight: bold; font-size: 12px;">[Job Title] | <span style="font-weight: normal;">[Company]</span></div>
      <div style="font-style: italic; font-size: 11px;">[Dates]</div>
    </div>
    <ul style="margin: 4px 0 0 0; padding-left: 18px; text-align: justify;">
      <li>[Bullet point tailored to JD]</li>
    </ul>
  </div>

  <h3 style="font-size: 12px; color: #6b21a8; border-bottom: 1px solid #6b21a8; margin: 12px 0 6px 0; text-transform: uppercase; font-weight: bold;">Education</h3>
  <div style="display: flex; justify-content: space-between; align-items: baseline;">
    <div style="font-weight: bold; font-size: 12px;">[Degree] | <span style="font-weight: normal;">[University]</span></div>
    <div style="font-style: italic; font-size: 11px;">[Year]</div>
  </div>
</div>

Fill in the template with the candidate's tailored information. Return ONLY the raw HTML code starting with <div style="font-family... Do not include any markdown wrappers like ```html.
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
