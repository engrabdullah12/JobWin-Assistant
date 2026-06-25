import os

files = [
    'ats/skill_extractor.py',
    'cover_letter/generator.py',
    'roadmap/roadmap_generator.py',
    'agents/resume_agent.py',
    'agents/router_agent.py',
    'rag/retriever.py',
]

for f in files:
    content = open(f, 'r', encoding='utf-8').read()
    content = content.replace('import openai', 'from groq import Groq')
    content = content.replace('client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))', 'client = Groq(api_key=os.getenv("GROQ_API_KEY"))')
    content = content.replace('model="gpt-3.5-turbo"', 'model="llama3-8b-8192"')
    open(f, 'w', encoding='utf-8').write(content)
    print(f'Updated: {f}')

print('Done! All files switched to Groq.')