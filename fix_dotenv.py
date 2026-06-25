import os

env_path = "D:/Ai-Recruitment-Copilot/AI-Recruitment-Copilot/.env"

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
    content = content.replace(
        'load_dotenv()',
        f'load_dotenv(dotenv_path="{env_path}")'
    )
    open(f, 'w', encoding='utf-8').write(content)
    print(f'Fixed: {f}')

print('All done!')