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
    content = content.replace('model="llama3-8b-8192"', 'model="llama-3.3-70b-versatile"')
    open(f, 'w', encoding='utf-8').write(content)
    print(f'Updated: {f}')

print('Done!')