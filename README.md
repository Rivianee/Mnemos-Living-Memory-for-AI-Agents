# Mnemos 
🧠 Mnemos — Living Memory for AI Agents
<div align="center">
Memory that evolves, learns, and forgets — just like a human brain.
Mostrar Imagem
Mostrar Imagem
Mostrar Imagem
</div>

🐟 The Problem
You spend 1 hour configuring your AI agent. You explain your preferences, your project, your context.
Next session? It remembers nothing.
LLMs have a goldfish memory problem:

They only remember what fits in the context window
Long conversations = important details get dropped
Every new session starts from zero

Existing solutions (RAG, summaries, vector stores) help — but they're static. They store. They don't evolve.

✨ What Mnemos Does Differently
<div align="center">
FeatureRAG / ChromaDBMemPalaceMnemosSemantic search✅✅✅Organized structure❌✅✅Dynamic importance❌❌✅Forgetting curve❌❌✅Graph reorganization❌❌✅Persists across sessions✅✅✅
</div>

MemPalace organizes memory. Mnemos makes memory evolve.


🏛️ How It Works
Room: user/preferences     → "prefers short answers"        importance: 0.95 ████░
Room: project/goals        → "build Mnemos for GitHub"      importance: 0.90 ████░
Room: knowledge/science    → "Ebbinghaus forgetting curve"  importance: 0.70 ███░░
Room: personal/tasks       → "buy coffee tomorrow"          importance: 0.10 █░░░░ ✕

🏠 Rooms — organize memories by context (project/myapp, user/preferences)
🔍 Semantic search — finds memories by meaning, not exact words
📊 PageRank graph — frequently accessed memories become more central
💤 Ebbinghaus forgetting — weak memories fade, important ones survive
💾 Persistence — everything survives restarts


🚀 Quickstart
Install
bashgit clone https://github.com/Rivianee/Mnemos-Living-Memory-for-AI-Agents
cd Mnemos-Living-Memory-for-AI-Agents
pip install -e .
CLI
bashmnemos status
mnemos remember "User prefers concise responses" --room user/preferences --importance 0.95
mnemos recall "how should I respond?"
mnemos consolidate
Visual Demo
bashpip install streamlit
streamlit run app.py
Use in Your Agent
pythonfrom mnemos.engine import EvoPalace

palace = EvoPalace(
    palace_name="my_agent",
    api_key="YOUR_GOOGLE_API_KEY",  # free at aistudio.google.com
    persist_path="./memory",
)

# Store
palace.remember(
    "User prefers concise responses, no bullet points",
    room="user/preferences",
    importance=0.95,
)

# Recall
results = palace.recall("how should I respond to this user?", top_k=3)
for r in results:
    print(r["content"])

# Evolve
palace.reorganize()   # PageRank redistributes importance
palace.consolidate()  # Ebbinghaus removes weak memories

🔑 Free API Key

Go to aistudio.google.com/apikey
Sign in with Google → Create API key
Pass it as api_key= or set GOOGLE_API_KEY env variable


Works without a key too — offline mode uses hash-based embeddings.


📋 API Reference
EvoPalace(palace_name, api_key, persist_path, forget_threshold)
ParameterDefaultDescriptionpalace_name"MyPalace"Identifier for this memory palaceapi_keyNoneGoogle Gemini API keypersist_path"./evopalace_data"Where to save dataforget_threshold0.15Score below which memories are forgotten
Methods
MethodDescriptionremember(content, room, tags, importance)Store a new memoryrecall(query, top_k, room_filter)Semantic searchlink(id_a, id_b, relation)Connect two memoriesreorganize()PageRank redistributes importanceconsolidate(dry_run)Apply forgetting curvestatus()Palace overviewlist_all()All memories sorted by importance

✅ MVP Validation — 9/9 Tests Passing
✅ Saves memories in different rooms
✅ Rooms created correctly
✅ Memories survive restart (persistence)
✅ Rooms survive restart
✅ Semantic search — finds correct memory
✅ Semantic search — finds user preferences
✅ Weak memory forgotten (Ebbinghaus curve)
✅ Important memories survived consolidation
✅ Important memory still searchable after consolidation
bashpython mvp.py

🗂️ Project Structure
Mnemos/
├── mnemos/
│   ├── __init__.py      ← package
│   ├── engine.py        ← core memory engine
│   └── cli.py           ← command line interface
├── app.py               ← Streamlit visual demo
├── mvp.py               ← validation (9/9 tests)
├── pyproject.toml
├── requirements.txt
└── README.md

🛣️ Roadmap

 pip install mnemos on PyPI
 REST API — use Mnemos without running locally
 LangGraph / CrewAI integration
 Multi-agent shared memory palace
 Cloud hosted version


🧰 Stack
ChromaDB · NetworkX · Google Gemini · Streamlit · Click

📄 License
MIT — free to use, modify, and build on.

<div align="center">
Built as an evolution of MemPalace — taking the memory palace concept further with dynamic, living memory.
⭐ If this helped you, consider starring the repo
</div>
