import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ats.skill_extractor import extract_text_from_pdf, extract_skills
from ats.ats_score import calculate_ats_score
from cover_letter.generator import generate_cover_letter
from roadmap.roadmap_generator import generate_roadmap, generate_interview_questions
from agents.resume_agent import resume_agent
from agents.router_agent import router_agent
from rag.qdrant_store import create_collection, store_document
from rag.retriever import ask_with_rag

st.set_page_config(page_title="AI Recruitment Copilot", page_icon="🤖", layout="wide")

st.sidebar.title("🤖 AI Recruitment Copilot")
page = st.sidebar.radio("Navigate", [
    "🏠 Dashboard",
    "📄 Resume Analysis",
    "✉️ Cover Letter",
    "❓ Interview Questions",
    "🗺️ Learning Roadmap",
    "💬 AI Chatbot"
])

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if "jd_text" not in st.session_state:
    st.session_state.jd_text = ""
if "ats_result" not in st.session_state:
    st.session_state.ats_result = None

st.sidebar.markdown("---")
st.sidebar.subheader("Upload Files")
resume_file = st.sidebar.file_uploader("Upload Resume PDF", type=["pdf"])

if resume_file:
    with open("data/uploads/resume.pdf", "wb") as f:
        f.write(resume_file.read())
    st.session_state.resume_text = extract_text_from_pdf("data/uploads/resume.pdf")
    st.sidebar.success("Resume uploaded!")

st.sidebar.markdown("---")
st.sidebar.subheader("Job Description")
jd_input = st.sidebar.text_area("Paste Job Description here", height=200)
if st.sidebar.button("Save JD"):
    if jd_input.strip():
        st.session_state.jd_text = jd_input.strip()
        st.sidebar.success("JD saved!")
    else:
        st.sidebar.error("Please paste a job description first.")

if page == "🏠 Dashboard":
    st.title("🤖 AI Recruitment Copilot")
    st.markdown("### Your AI-powered job application assistant")
    st.markdown("---")
    if st.session_state.resume_text and st.session_state.jd_text:
        if st.button("Run Full ATS Analysis"):
            with st.spinner("Analyzing..."):
                resume_skills = extract_skills(st.session_state.resume_text, "resume")
                jd_skills = extract_skills(st.session_state.jd_text, "job description")
                result = calculate_ats_score(resume_skills, jd_skills)
                st.session_state.ats_result = result
        if st.session_state.ats_result:
            result = st.session_state.ats_result
            col1, col2, col3 = st.columns(3)
            col1.metric("ATS Score", f"{result['ats_score']}%")
            col2.metric("Matched Skills", result['total_matched'])
            col3.metric("Missing Skills", len(result['missing_skills']))
            st.markdown("---")
            col4, col5 = st.columns(2)
            with col4:
                st.subheader("Matched Skills")
                for skill in result['matched_skills']:
                    st.success(skill)
            with col5:
                st.subheader("Missing Skills")
                for skill in result['missing_skills']:
                    st.error(skill)
    else:
        st.info("Upload your Resume and paste Job Description from the sidebar to get started!")

elif page == "📄 Resume Analysis":
    st.title("Resume Analysis")
    st.markdown("---")
    if st.session_state.resume_text:
        if st.button("Analyze My Resume"):
            with st.spinner("Analyzing resume..."):
                analysis = resume_agent(st.session_state.resume_text)
            st.markdown(analysis)
    else:
        st.warning("Please upload your resume from the sidebar first.")

elif page == "✉️ Cover Letter":
    st.title("Cover Letter Generator")
    st.markdown("---")
    if st.session_state.resume_text and st.session_state.jd_text:
        if st.button("Generate Cover Letter"):
            with st.spinner("Writing cover letter..."):
                letter = generate_cover_letter(
                    st.session_state.resume_text,
                    st.session_state.jd_text
                )
            st.text_area("Your Cover Letter", letter, height=400)
            st.download_button("Download", letter, file_name="cover_letter.txt")
    else:
        st.warning("Please upload Resume and paste JD from the sidebar first.")

elif page == "❓ Interview Questions":
    st.title("Interview Question Generator")
    st.markdown("---")
    if st.session_state.resume_text and st.session_state.jd_text:
        if st.button("Generate Questions"):
            with st.spinner("Generating questions..."):
                questions = generate_interview_questions(
                    st.session_state.resume_text,
                    st.session_state.jd_text
                )
            st.markdown(questions)
    else:
        st.warning("Please upload Resume and paste JD from the sidebar first.")

elif page == "🗺️ Learning Roadmap":
    st.title("Learning Roadmap Generator")
    st.markdown("---")
    if st.session_state.ats_result:
        missing = st.session_state.ats_result['missing_skills']
        st.subheader("Missing Skills")
        st.write(missing)
        if st.button("Generate Roadmap"):
            with st.spinner("Creating your roadmap..."):
                roadmap = generate_roadmap(missing)
            st.markdown(roadmap)
    else:
        st.warning("Please run ATS Analysis from the Dashboard first.")

elif page == "💬 AI Chatbot":
    st.title("AI Career Chatbot")
    st.markdown("---")
    create_collection()
    if st.session_state.resume_text:
        store_document(st.session_state.resume_text, {"type": "resume"})
    if st.session_state.jd_text:
        store_document(st.session_state.jd_text, {"type": "jd"})
    user_query = st.text_input("Ask anything about your resume or job...")
    if st.button("Ask"):
        if user_query:
            with st.spinner("Thinking..."):
                answer = router_agent(
                    user_query,
                    resume_text=st.session_state.resume_text,
                    jd_text=st.session_state.jd_text,
                    missing_skills=st.session_state.ats_result['missing_skills'] if st.session_state.ats_result else []
                )
            st.markdown(answer)
