files = {
"ats/skill_extractor.py": """import pdfplumber
import openai
import os
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_skills(text, source="resume"):
    prompt = f\"\"\"
You are an expert HR analyst.
Extract all technical skills from this {source} text.
Return ONLY a Python list like: ['Python', 'SQL', 'Docker']
No explanation. Just the list.

Text:
{text}
\"\"\"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    raw = response.choices[0].message.content.strip()
    skills = eval(raw)
    return skills
""",

"ats/ats_score.py": """def calculate_ats_score(resume_skills, jd_skills):
    resume_set = set([s.lower() for s in resume_skills])
    jd_set = set([s.lower() for s in jd_skills])
    matched = resume_set.intersection(jd_set)
    missing = jd_set - resume_set
    score = round((len(matched) / len(jd_set)) * 100) if jd_set else 0
    return {
        "ats_score": score,
        "matched_skills": list(matched),
        "missing_skills": list(missing),
        "total_jd_skills": len(jd_set),
        "total_matched": len(matched)
    }
""",

"cover_letter/generator.py": """import openai
import os
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_cover_letter(resume_text, jd_text):
    prompt = f\"\"\"
You are a professional cover letter writer.
Write a compelling cover letter based on this resume and job description.
Resume: {resume_text}
Job Description: {jd_text}
Write a professional cover letter under 300 words.
\"\"\"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
""",

"roadmap/roadmap_generator.py": """import openai
import os
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_roadmap(missing_skills):
    skills_list = ", ".join(missing_skills)
    prompt = f\"\"\"
You are a career coach.
Create a 30-day learning roadmap to learn: {skills_list}
Format week by week:
Week 1: ...
Week 2: ...
Week 3: ...
Week 4: ...
\"\"\"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def generate_interview_questions(resume_text, jd_text):
    prompt = f\"\"\"
You are an expert interviewer.
Generate 10 interview questions based on this resume and job description.
Mix technical and behavioral questions.
Resume: {resume_text}
Job Description: {jd_text}
Return as a numbered list.
\"\"\"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
""",

"agents/resume_agent.py": """import openai
import os
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def resume_agent(resume_text):
    prompt = f\"\"\"
You are an expert resume reviewer.
Analyze this resume and provide:
1. Overall strength (out of 10)
2. Key strengths
3. Weaknesses
4. Suggestions to improve
Resume: {resume_text}
\"\"\"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
""",

"agents/ats_agent.py": """from ats.skill_extractor import extract_skills
from ats.ats_score import calculate_ats_score

def ats_agent(resume_text, jd_text):
    resume_skills = extract_skills(resume_text, source="resume")
    jd_skills = extract_skills(jd_text, source="job description")
    result = calculate_ats_score(resume_skills, jd_skills)
    return result
""",

"agents/interview_agent.py": """from roadmap.roadmap_generator import generate_interview_questions

def interview_agent(resume_text, jd_text):
    questions = generate_interview_questions(resume_text, jd_text)
    return questions
""",

"agents/career_agent.py": """from roadmap.roadmap_generator import generate_roadmap

def career_agent(missing_skills):
    roadmap = generate_roadmap(missing_skills)
    return roadmap
""",

"agents/router_agent.py": """import openai
import os
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def router_agent(user_query, resume_text="", jd_text="", missing_skills=[]):
    prompt = f\"\"\"
You are a router. Based on the user query, decide which agent to call.
Return ONLY one of these words: resume_agent, ats_agent, interview_agent, career_agent
User Query: {user_query}
\"\"\"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    agent_name = response.choices[0].message.content.strip().lower()

    if agent_name == "resume_agent":
        from agents.resume_agent import resume_agent
        return resume_agent(resume_text)
    elif agent_name == "ats_agent":
        from agents.ats_agent import ats_agent
        return ats_agent(resume_text, jd_text)
    elif agent_name == "interview_agent":
        from agents.interview_agent import interview_agent
        return interview_agent(resume_text, jd_text)
    elif agent_name == "career_agent":
        from agents.career_agent import career_agent
        return career_agent(missing_skills)
    else:
        return "Sorry, I could not understand your request."
""",

"rag/embeddings.py": """from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text):
    embedding = model.encode(text)
    return embedding.tolist()
""",

"rag/qdrant_store.py": """from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from rag.embeddings import get_embedding
import uuid

client = QdrantClient(":memory:")
COLLECTION_NAME = "recruitment_kb"

def create_collection():
    existing = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME not in existing:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )

def store_document(text, metadata={}):
    embedding = get_embedding(text)
    point = PointStruct(
        id=str(uuid.uuid4()),
        vector=embedding,
        payload={"text": text, **metadata}
    )
    client.upsert(collection_name=COLLECTION_NAME, points=[point])

def search_documents(query, top_k=3):
    embedding = get_embedding(query)
    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=embedding,
        limit=top_k
    )
    return [r.payload["text"] for r in results]
""",

"rag/retriever.py": """import openai
import os
from dotenv import load_dotenv
from rag.qdrant_store import search_documents

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_with_rag(question):
    chunks = search_documents(question, top_k=3)
    context = "\\n\\n".join(chunks)
    prompt = f\"\"\"
You are a helpful career assistant.
Use the following context to answer the question.
Context: {context}
Question: {question}
Answer:
\"\"\"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
""",
}

for filepath, content in files.items():
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {filepath}")

print("\nAll files created successfully!")