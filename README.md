# 🧠 Mnemos — Living Memory for AI Agents

<div align="center">

**Memory that evolves, learns, and forgets — just like a human brain.**

[![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Stars](https://img.shields.io/github/stars/Rivianee/Mnemos-Living-Memory-for-AI-Agents?style=flat-square)](https://github.com/Rivianee/Mnemos-Living-Memory-for-AI-Agents/stargazers)

</div>

---

## 🐟 The Problem

You spend 1 hour configuring your AI agent. You explain your preferences, your project, your context.

**Next session? It remembers nothing.**

LLMs have a goldfish memory problem:
- They only remember what fits in the context window
- Long conversations = important details get dropped
- Every new session starts from zero

Existing solutions (RAG, summaries, vector stores) help — but they're **static**. They store. They don't **evolve**.

---

## ✨ What Mnemos Does Differently

<div align="center">

| Feature | RAG / ChromaDB | MemPalace | **Mnemos** |
|---|:---:|:---:|:---:|
| Semantic search | ✅ | ✅ | ✅ |
| Organized structure | ❌ | ✅ | ✅ |
| Dynamic importance | ❌ | ❌ | ✅ |
| Forgetting curve | ❌ | ❌ | ✅ |
| Graph reorganization | ❌ | ❌ | ✅ |
| Persists across sessions | ✅ | ✅ | ✅ |

</div>

> **MemPalace organizes memory. Mnemos makes memory evolve.**

---

## 🏛️ How It Works

```
Room: user/preferences     → "prefers short answers"        importance: 0.95 ████░
Room: project/goals        → "build Mnemos for GitHub"      importance: 0.90 ████░
Room: knowledge/science    → "Ebbinghaus forgetting curve"  importance: 0.70 ███░░
Room: personal/tasks       → "buy coffee tomorrow"          importance: 0.10 █░░░░ ✕
```

- 🏠 **Rooms** — organize memories by context (`project/myapp`, `user/preferences`)
- 🔍 **Semantic search** — finds memories by meaning, not exact words
- 📊 **PageRank graph** — frequently accessed memories become more central
- 💤 **Ebbinghaus forgetting** — weak memories fade, important ones survive
- 💾 **Persistence** — everything survives restarts

---

## 🚀 Quickstart

### Install

```bash
git clone https://github.com/Rivianee/Mnemos-Living-Memory-for-AI-Agents
cd Mnemos-Living-Memory-for-AI-Agents
pip install -e .
```

### CLI

```bash
mnemos status
mnemos remember "User prefers concise responses" --room user/preferences --importance 0.95
mnemos recall "how should I respond?"
mnemos consolidate
```

### Visual Demo

```bash
pip install streamlit
streamlit run app.py
```

### Use in Your Agent

```python
from mnemos.engine import EvoPalace

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
```

---

## 🔑 Free API Key

1. Go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Sign in with Google → **Create API key**
3. Pass it as `api_key=` or set `GOOGLE_API_KEY` env variable

> Works without a key too — offline mode uses hash-based embeddings.

---

## 📋 API Reference

### `EvoPalace(palace_name, api_key, persist_path, forget_threshold)`

| Parameter | Default | Description |
|---|---|---|
| `palace_name` | `"MyPalace"` | Identifier for this memory palace |
| `api_key` | `None` | Google Gemini API key |
| `persist_path` | `"./evopalace_data"` | Where to save data |
| `forget_threshold` | `0.15` | Score below which memories are forgotten |

### Methods

| Method | Description |
|---|---|
| `remember(content, room, tags, importance)` | Store a new memory |
| `recall(query, top_k, room_filter)` | Semantic search |
| `link(id_a, id_b, relation)` | Connect two memories |
| `reorganize()` | PageRank redistributes importance |
| `consolidate(dry_run)` | Apply forgetting curve |
| `status()` | Palace overview |
| `list_all()` | All memories sorted by importance |

---

## ✅ MVP Validation — 9/9 Tests Passing

```
✅ Saves memories in different rooms
✅ Rooms created correctly
✅ Memories survive restart (persistence)
✅ Rooms survive restart
✅ Semantic search — finds correct memory
✅ Semantic search — finds user preferences
✅ Weak memory forgotten (Ebbinghaus curve)
✅ Important memories survived consolidation
✅ Important memory still searchable after consolidation
```

```bash
python mvp.py
```

---

## 🗂️ Project Structure

```
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
```

---

## 🛣️ Roadmap

- [ ] `pip install mnemos` on PyPI
- [ ] REST API — use Mnemos without running locally
- [ ] LangGraph / CrewAI integration
- [ ] Multi-agent shared memory palace
- [ ] Cloud hosted version

---

## MCP Server — Connect to Cursor, Claude Code, Windsurf

### Install
\```
pip install -r requirements.txt
\```

### Configure (Claude Code / Claude Desktop)
Add to your `claude_desktop_config.json`:
\```json
{
  "mcpServers": {
    "mnemos": {
      "command": "python",
      "args": ["/path/to/mcp_server.py"],
      "env": {
        "GOOGLE_API_KEY": "optional"
      }
    }
  }
}
\```

### Available tools
| Tool | Description |
|---|---|
| `remember` | Store a memory |
| `recall` | Search by meaning |
| `forget` | Apply Ebbinghaus curve |
| `reorganize` | Run PageRank |
| `status` | Palace overview |
| `link` | Connect two memories |

## 🧰 Stack

**[ChromaDB](https://www.trychroma.com/)** · **[NetworkX](https://networkx.org/)** · **[Google Gemini](https://aistudio.google.com/)** · **[Streamlit](https://streamlit.io/)** · **[Click](https://click.palletsprojects.com/)**

---

## 📄 License

MIT — free to use, modify, and build on.

---

<div align="center">

Built as an evolution of [MemPalace](https://github.com/milla-jovovich/mempalace) — taking the memory palace concept further with **dynamic, living memory**.

⭐ If this helped you, consider starring the repo

</div>
