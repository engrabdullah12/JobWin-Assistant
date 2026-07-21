from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

# Internal imports
from ats.skill_extractor import extract_text_from_pdf, extract_skills
from ats.ats_score import calculate_ats_score
from cover_letter.generator import generate_cover_letter
from roadmap.roadmap_generator import generate_roadmap, generate_interview_questions
from agents.resume_agent import resume_agent
from agents.router_agent import router_agent
from agents.upwork_agent import generate_upwork_proposal
from agents.resume_tailor_agent import tailor_resume
from rag.qdrant_store import create_collection, store_document
import os
import shutil

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class JDRequest(BaseModel):
    resume_text: Optional[str] = ""
    jd_text: str

class RoadmapRequest(BaseModel):
    missing_skills: List[str]

class UpworkRequest(BaseModel):
    resume_text: str
    jd_text: str
    hiring_rate: str
    payment_verified: bool
    other_notes: str

class ChatRequest(BaseModel):
    user_query: str
    resume_text: str
    jd_text: str
    missing_skills: List[str]

@app.post("/api/upload_resume")
async def upload_resume(file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()
        text = extract_text_from_pdf(file_bytes)
        return {"text": text}
    except Exception as e:
        return {"error": str(e), "text": ""}

@app.post("/api/resume_analysis")
async def analyze_resume(req: JDRequest):
    analysis = resume_agent(req.resume_text)
    return {"analysis": analysis}

@app.post("/api/ats_analysis")
async def ats_analysis(req: JDRequest):
    resume_skills = extract_skills(req.resume_text, "resume")
    jd_skills = extract_skills(req.jd_text, "job description")
    result = calculate_ats_score(resume_skills, jd_skills, req.resume_text, req.jd_text)
    return {"result": result, "resume_skills": resume_skills}

@app.post("/api/cover_letter")
async def cover_letter(req: JDRequest):
    letter = generate_cover_letter(req.resume_text, req.jd_text)
    return {"cover_letter": letter}

@app.post("/api/interview_questions")
async def interview_questions(req: JDRequest):
    questions = generate_interview_questions(req.resume_text, req.jd_text)
    return {"questions": questions}

@app.post("/api/roadmap")
async def roadmap(req: RoadmapRequest):
    roadmap_text = generate_roadmap(req.missing_skills)
    return {"roadmap": roadmap_text}

@app.post("/api/upwork_proposal")
async def upwork_proposal(req: UpworkRequest):
    proposal = generate_upwork_proposal(
        req.resume_text, 
        req.jd_text, 
        req.hiring_rate, 
        req.payment_verified, 
        req.other_notes
    )
    return {"proposal": proposal}

@app.post("/api/tailor_resume")
async def api_tailor_resume(req: JDRequest):
    html_resume = tailor_resume(req.resume_text, req.jd_text)
    return {"html": html_resume}

@app.post("/api/chat")
async def chat(req: ChatRequest):
    create_collection()
    if req.resume_text:
        store_document(req.resume_text, {"type": "resume"})
    if req.jd_text:
        store_document(req.jd_text, {"type": "jd"})
    answer = router_agent(
        req.user_query,
        req.resume_text,
        req.jd_text,
        req.missing_skills
    )
    return {"answer": answer}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
