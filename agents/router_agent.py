import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3.1-flash-lite")

def router_agent(user_query, resume_text="", jd_text="", missing_skills=[]):
    prompt = f"""You are a router. Based on the user query, decide which agent to call.
Return ONLY one of these words: resume_agent, ats_agent, interview_agent, career_agent
User Query: {user_query}"""
    response = model.generate_content(prompt)
    agent_name = response.text.strip().lower()

    if "resume_agent" in agent_name:
        from agents.resume_agent import resume_agent
        return resume_agent(resume_text)
    elif "ats_agent" in agent_name:
        from agents.ats_agent import ats_agent
        return ats_agent(resume_text, jd_text)
    elif "interview_agent" in agent_name:
        from agents.interview_agent import interview_agent
        return interview_agent(resume_text, jd_text)
    elif "career_agent" in agent_name:
        from agents.career_agent import career_agent
        return career_agent(missing_skills)
    else:
        return "Sorry, I could not understand your request."
