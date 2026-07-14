import google.generativeai as genai
import os
import io
import re
from dotenv import load_dotenv
from xhtml2pdf import pisa
from PyPDF2 import PdfReader

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3.1-flash-lite")

# ---------- 1. CSS Template (controlled directly for best PDF outputs) ----------
def build_css(font_size, line_height, section_gap):
    return f"""
    <style>
      @page {{ size: A4; margin: 12mm 16mm; }}
      * {{ box-sizing: border-box; }}
      body {{
        font-family: Helvetica, Arial, sans-serif;
        color: #000; background: #fff;
        font-size: {font_size}pt;
        line-height: {line_height};
      }}
      h1 {{
        text-align:center; font-size:{font_size + 11}pt;
        margin:0 0 2px 0; letter-spacing:0.5px;
      }}
      .title {{
        text-align:center; color:#6b21a8; font-weight:bold;
        font-size:{font_size + 2}pt; margin:0 0 4px 0;
      }}
      .contact {{
        text-align:center; font-size:{font_size - 1}pt;
        margin-bottom:{section_gap}pt; color:#333;
      }}
      h2 {{
        text-align:center; text-transform:uppercase; color:#6b21a8;
        font-size:{font_size + 1}pt; border-bottom:1px solid #6b21a8;
        margin:{section_gap}pt 0 4px 0;
      }}
      p {{ margin:2px 0; }}
      ul {{ margin:2px 0 {section_gap * 0.6}pt 18px; padding:0; }}
      li {{ margin-bottom:2px; }}
      table {{ border-collapse: collapse; margin-bottom: 2px; }}
      td {{ padding: 0; vertical-align: top; }}
    </style>
    """

def wrap_full_html(inner_html, font_size, line_height, section_gap):
    css = build_css(font_size, line_height, section_gap)
    return f"<html><head><meta charset='utf-8'>{css}</head><body>{inner_html}</body></html>"

# Convert flexbox headers to tables for xhtml2pdf compatibility
def format_job_headers(html_content):
    pattern = r'<div class="job-header">\s*<span class="job-title">(.*?)</span>\s*<span class="job-date">(.*?)</span>\s*</div>'
    replacement = r'<table style="width:100%; border:none; margin-bottom:2px;"><tr><td style="font-weight:bold; text-align:left;">\1</td><td style="font-style:italic; text-align:right; white-space:nowrap;">\2</td></tr></table>'
    return re.sub(pattern, replacement, html_content)

# ---------- 2. Content generation — LLM provides semantic HTML content ----------
def generate_resume_content(resume_text, jd_text):
    prompt = f"""You are an expert technical resume writer.
Rewrite the candidate's resume to match the Job Description as closely as possible,
staying truthful (don't invent jobs, but reframe/highlight relevant real experience).

### Job Description:
{jd_text}

### Original Resume:
{resume_text}

### Output rules (VERY IMPORTANT):
- Output ONLY semantic HTML content, NO <style>, NO inline style="", NO CSS at all.
- Use ONLY these tags/classes so they map to a fixed template:
  <h1> for name
  <p class="title"> for job title
  <p class="contact"> for contact line (location | email | phone)
  <h2> for section headers (SUMMARY, WORK EXPERIENCE, PROJECTS, TECHNICAL SKILLS, EDUCATION)
  <div class="job-header"><span class="job-title">Role — Company</span><span class="job-date">2022 – Present</span></div>
  <ul><li>...</li></ul> for bullet points
- BE CONCISE: max 3-4 bullets per job, each bullet max 1 line (~15-18 words).
- Do NOT pad with filler sentences. Prioritize the most JD-relevant points only.
- No markdown, no ```html fences. Return raw HTML starting with <div class="resume-container">.
"""
    response = model.generate_content(prompt)
    return clean_html(response.text)

def clean_html(text):
    text = text.strip()
    if text.startswith("```html"):
        text = text[7:]
    if text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()

# ---------- 3. Shrink-to-fit loop ----------
def count_pdf_pages(pdf_bytes):
    reader = PdfReader(io.BytesIO(pdf_bytes))
    return len(reader.pages)

def html_to_pdf_bytes(html_string):
    pdf_io = io.BytesIO()
    pisa.CreatePDF(html_string, dest=pdf_io)
    return pdf_io.getvalue()

def fit_to_one_page(inner_html, max_font=11.0, min_font=8.0, step=0.5):
    font_size = max_font
    line_height = 1.3
    section_gap = 8

    last_pdf = None
    last_html = None

    formatted_inner = format_job_headers(inner_html)

    while font_size >= min_font:
        full_html = wrap_full_html(formatted_inner, font_size, line_height, section_gap)
        pdf_bytes = html_to_pdf_bytes(full_html)
        pages = count_pdf_pages(pdf_bytes)

        last_pdf, last_html = pdf_bytes, full_html

        if pages <= 1:
            return full_html, pdf_bytes

        # shrink layout properties and try again
        font_size -= step
        line_height = max(1.1, line_height - 0.03)
        section_gap = max(4, section_gap - 0.5)

    return last_html, last_pdf

# ---------- 4. Main entry point ----------
def tailor_resume(resume_text, jd_text):
    inner_html = generate_resume_content(resume_text, jd_text)
    final_html, final_pdf_bytes = fit_to_one_page(inner_html)
    return final_html, final_pdf_bytes