"""
Demo do EvoPalace — rode com: python demo.py
Não precisa de API key, funciona em modo offline.
Para usar Google Gemini: export GOOGLE_API_KEY=sua_chave
"""

from engine import EvoPalace
import pprint

print("=" * 55)
print("  EvoPalace Demo — Palácio de Memória Vivo")
print("=" * 55)

# ── 1. Inicializa o palácio ──────────────────────────────
palace = EvoPalace(
    palace_name="demo_palace",
    persist_path="./demo_data",
    forget_threshold=0.10,  # baixo para demo
)

# ── 2. Grava memórias em quartos diferentes ──────────────
print("\n📥 Gravando memórias...\n")

palace.remember(
    "EvoPalace é um sistema de memória dinâmica para agentes de IA",
    room="projeto/evopalace",
    tags=["evopalace", "conceito", "core"],
    importance=0.9,
)
palace.remember(
    "A curva de Ebbinghaus modela como humanos esquecem informações ao longo do tempo",
    room="conhecimento/psicologia",
    tags=["ebbinghaus", "esquecimento", "ciencia"],
    importance=0.7,
)
palace.remember(
    "O MemPalace usa ChromaDB com hierarquia wings > halls > rooms",
    room="projeto/concorrentes",
    tags=["mempalace", "chromadb", "referencia"],
    importance=0.6,
)
palace.remember(
    "Riviane está construindo o EvoPalace para portfólio e produto",
    room="usuario/riviane",
    tags=["riviane", "meta", "objetivo"],
    importance=0.85,
)
palace.remember(
    "NetworkX permite calcular PageRank para descobrir memórias mais centrais",
    room="projeto/evopalace",
    tags=["networkx", "grafo", "pagerank"],
    importance=0.75,
)
palace.remember(
    "Lembrar de comprar café amanhã",
    room="pessoal/tarefas",
    tags=["tarefa", "efemero"],
    importance=0.2,
)

# ── 3. Estado inicial ────────────────────────────────────
print("\n📊 Status do Palácio:\n")
pprint.pprint(palace.status())

# ── 4. Busca semântica ───────────────────────────────────
print("\n🔍 Buscando: 'como funciona o esquecimento'\n")
results = palace.recall("como funciona o esquecimento", top_k=3)
for r in results:
    print(f"  [{r['id']}] room={r['room']} | importance={r['importance']} | dist={r['distance']}")
    print(f"  → {r['content'][:70]}")
    print()

# ── 5. Criando ligação manual entre memórias ─────────────
print("🔗 Criando ligação entre memórias relacionadas...\n")
if len(palace._meta) >= 2:
    ids = list(palace._meta.keys())
    palace.link(ids[0], ids[1], relation="inspira", weight=0.9)

# ── 6. Reorganização dinâmica (grafo) ────────────────────
print("\n↺ Reorganizando com PageRank...\n")
changes = palace.reorganize()
if changes:
    for mem_id, diff in changes.items():
        print(f"  [{mem_id}] importance: {diff['old']} → {diff['new']}")

# ── 7. Consolidação (esquecimento) ───────────────────────
print("\n💤 Simulando consolidação (dry_run)...\n")
result = palace.consolidate(dry_run=True)
print(f"  Seriam esquecidas: {len(result['forgotten'])} memórias")
for mem_id, score in result["forgotten"]:
    print(f"  [{mem_id}] score={score}")

# ── 8. Lista final ───────────────────────────────────────
print("\n📋 Todas as memórias (ordenadas por importância):\n")
for m in palace.list_all():
    bar = "█" * int(m["importance"] * 10) + "░" * (10 - int(m["importance"] * 10))
    print(f"  [{m['id']}] {bar} {m['importance']} | {m['room']}")
    print(f"  → {m['content'][:65]}")
    print()

print("=" * 55)
print("✅ Demo concluído! Dados salvos em ./demo_data/")
print("=" * 55)
