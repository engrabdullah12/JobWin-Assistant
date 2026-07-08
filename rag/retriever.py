import google.generativeai as genai
import os
from dotenv import load_dotenv
from rag.qdrant_store import search_documents

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3.1-flash-lite")

def ask_with_rag(question):
    chunks = search_documents(question, top_k=3)
    context = "\n\n".join(chunks)
    prompt = f"""You are a helpful career assistant.
Use the following context to answer the question.
Context: {context}
Question: {question}
Answer:"""
    response = model.generate_content(prompt)
    return response.text.strip()
