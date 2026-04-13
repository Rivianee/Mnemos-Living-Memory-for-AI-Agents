# 🧠 Mnemos — Living Memory for AI Agents

> Memory that evolves, learns, and forgets — just like a human brain.

Most AI agents forget everything after a few messages. Mnemos fixes that.

---

## The Problem

LLMs have a goldfish memory problem:

- They only "remember" what fits in the context window
- Long conversations = important details get dropped
- Every new session starts from zero

Existing solutions (RAG, summaries, vector stores) help — but they're static. They store. They don't **evolve**.

---

## What Mnemos Does Differently

| Feature | RAG / ChromaDB | MemPalace | **Mnemos** |
|---|---|---|---|
| Semantic search | ✅ | ✅ | ✅ |
| Organized structure | ❌ | ✅ | ✅ |
| Dynamic importance | ❌ | ❌ | ✅ |
| Forgetting curve | ❌ | ❌ | ✅ |
| Graph-based reorganization | ❌ | ❌ | ✅ |
| Persists across sessions | ✅ | ✅ | ✅ |

**MemPalace organizes memory. Mnemos makes memory evolve.**

---

## How It Works

```
Wing → Hall → Room → Memory
```

- **Rooms** organize memories by topic (`project/myapp`, `user/preferences`)
- **Semantic search** finds memories by meaning, not just keywords
- **PageRank** on a graph makes frequently-accessed memories more central
- **Ebbinghaus forgetting curve** removes weak memories over time
- **Persistence** — everything survives restarts

---

## Quickstart

```bash
git clone https://github.com/yourusername/mnemos
cd mnemos
pip install -r requirements.txt
```

### Run the visual demo

```bash
streamlit run app.py
```

### Run the MVP validation (9/9 tests)

```bash
# Add your Google API key to mvp.py first (optional — works offline too)
python mvp.py
```

### Use in your own agent

```python
from engine import EvoPalace

palace = EvoPalace(
    palace_name="my_agent",
    api_key="YOUR_GOOGLE_API_KEY",  # optional, for real semantic search
    persist_path="./memory",
)

# Store a memory
palace.remember(
    "User prefers concise responses, no bullet points",
    room="user/preferences",
    tags=["style"],
    importance=0.95,
)

# Recall relevant memories
results = palace.recall("how should I respond to this user?", top_k=3)
for r in results:
    print(r["content"])

# Evolve — reorganize importance based on usage
palace.reorganize()

# Sleep — forget weak memories
palace.consolidate()
```

---

## API Reference

### `EvoPalace(palace_name, api_key, persist_path, forget_threshold)`

| Parameter | Default | Description |
|---|---|---|
| `palace_name` | `"MyPalace"` | Identifier for this memory palace |
| `api_key` | `None` | Google Gemini API key (free at aistudio.google.com) |
| `persist_path` | `"./evopalace_data"` | Where to save data on disk |
| `forget_threshold` | `0.15` | Memories below this score get forgotten |

### Methods

| Method | Description |
|---|---|
| `remember(content, room, tags, importance)` | Store a new memory |
| `recall(query, top_k, room_filter)` | Semantic search |
| `link(id_a, id_b, relation)` | Create explicit connection between memories |
| `reorganize()` | Run PageRank to redistribute importance |
| `consolidate(dry_run)` | Apply forgetting curve |
| `status()` | Palace overview |
| `list_all()` | All memories sorted by importance |

---

## MVP Validation

```
9/9 tests passing ✅

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

---

## Getting a Free API Key

1. Go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Sign in with Google
3. Click **Create API key**
4. Paste it into `mvp.py` or the Streamlit sidebar

Works without a key too — offline mode uses deterministic hash embeddings.

---

## Roadmap

- [ ] REST API (use Mnemos without running locally)
- [ ] Living skills (`.md` skill files that improve with usage)
- [ ] LangGraph / CrewAI integration
- [ ] Multi-agent shared memory
- [ ] Cloud hosted version

---

## Stack

- **ChromaDB** — vector storage
- **NetworkX** — graph + PageRank
- **Google Gemini** — embeddings (`gemini-embedding-001`)
- **Streamlit** — visual demo

---

## License

MIT — free to use, modify, and build on.

---

Built as an evolution of [MemPalace](https://github.com/milla-jovovich/mempalace) — taking the memory palace concept further with dynamic, living memory.
