"""
EvoPalace MVP — Validação completa em um arquivo só
Roda com: python mvp.py

Prova 4 coisas:
  1. Salva memórias em rooms diferentes
  2. Persiste no disco (fecha e reabre)
  3. Busca semântica retorna o certo
  4. Esquecimento: memória fraca some, forte fica
"""

import shutil, os, sys, time

# ── Limpa dados anteriores ────────────────────────────────
DATA_PATH = "./mvp_data"
if os.path.exists(DATA_PATH):
    shutil.rmtree(DATA_PATH)

from engine import EvoPalace

PASS = "✅"
FAIL = "❌"
results = []

def check(label, condition, detail=""):
    status = PASS if condition else FAIL
    results.append((status, label))
    print(f"  {status} {label}")
    if detail:
        print(f"     → {detail}")


print()
print("══════════════════════════════════════════════")
print("  EvoPalace MVP — Validação")
print("══════════════════════════════════════════════")

# ═══════════════════════════════════════════════════════════
# TESTE 1 — Salvar memórias
# ═══════════════════════════════════════════════════════════
print("\n[1/4] SALVAR MEMÓRIAS\n")

p = EvoPalace("mvp", persist_path=DATA_PATH, forget_threshold=0.15)

m1 = p.remember("Riviane prefere respostas curtas e sem enrolação",
    room="usuario/preferencias", tags=["estilo"], importance=0.95)
m2 = p.remember("O projeto se chama EvoPalace e vai virar produto no GitHub",
    room="projeto/objetivo", tags=["produto"], importance=0.90)
m3 = p.remember("Lembrar de comprar café amanhã",
    room="pessoal/tarefas", tags=["tarefa"], importance=0.10)  # fraca — vai ser esquecida

s = p.status()
check("3 memórias salvas", s["total_memories"] == 3, f"total={s['total_memories']}")
check("Rooms criados corretamente", len(s["rooms"]) == 3, str(s["rooms"]))


# ═══════════════════════════════════════════════════════════
# TESTE 2 — Persistência
# ═══════════════════════════════════════════════════════════
print("\n[2/4] PERSISTÊNCIA (fecha e reabre)\n")

del p  # mata o objeto

p2 = EvoPalace("mvp", persist_path=DATA_PATH)  # recria do zero
s2 = p2.status()

check("Memórias sobreviveram ao fechar", s2["total_memories"] == 3,
    f"encontrou {s2['total_memories']} de 3")
check("Rooms sobreviveram", "usuario/preferencias" in s2["rooms"],
    str(list(s2["rooms"].keys())))


# ═══════════════════════════════════════════════════════════
# TESTE 3 — Busca semântica
# ═══════════════════════════════════════════════════════════
print("\n[3/4] BUSCA SEMÂNTICA\n")

# Busca por algo relacionado ao projeto
r1 = p2.recall("qual o objetivo do projeto", top_k=1)
achou_projeto = r1 and "EvoPalace" in r1[0]["content"]
check("Busca 'objetivo do projeto' → achou memória correta",
    achou_projeto,
    r1[0]["content"][:60] if r1 else "nada retornado")

# Busca por preferências
r2 = p2.recall("como a pessoa gosta de ser respondida", top_k=1)
achou_pref = r2 and "Riviane" in r2[0]["content"]
check("Busca 'preferências de resposta' → achou memória correta",
    achou_pref,
    r2[0]["content"][:60] if r2 else "nada retornado")

# Nota honesta sobre modo offline
if not achou_pref:
    print("     ⚠️  Modo offline: embeddings são hash, não semântica real.")
    print("        Com Google Gemini (API key) a busca seria precisa.")


# ═══════════════════════════════════════════════════════════
# TESTE 4 — Esquecimento
# ═══════════════════════════════════════════════════════════
print("\n[4/4] ESQUECIMENTO (curva de Ebbinghaus)\n")

# Simula que a memória fraca não foi acessada há muito tempo
fraca_id = m3.id
p2._meta[fraca_id]["last_accessed"] = time.time() - (48 * 3600)  # 48h atrás
p2._meta[fraca_id]["access_count"] = 1
p2._save_meta()

antes = p2.status()["total_memories"]
resultado = p2.consolidate(dry_run=False)
depois = p2.status()["total_memories"]

check("Memória fraca (café) foi esquecida",
    depois < antes,
    f"antes={antes} → depois={depois}")
check("Memórias importantes sobreviveram",
    depois >= 2,
    f"restaram {depois} memórias")

# Confirma que as importantes ainda estão lá
r3 = p2.recall("EvoPalace projeto", top_k=1)
check("Memória importante ainda buscável após consolidação",
    r3 and "EvoPalace" in r3[0]["content"],
    r3[0]["content"][:60] if r3 else "não encontrada")


# ═══════════════════════════════════════════════════════════
# RESULTADO FINAL
# ═══════════════════════════════════════════════════════════
print()
print("══════════════════════════════════════════════")
passou = sum(1 for s, _ in results if s == PASS)
total = len(results)
print(f"  RESULTADO: {passou}/{total} testes passaram")
print()
for status, label in results:
    print(f"  {status} {label}")
print("══════════════════════════════════════════════")

if passou == total:
    print("\n  🚀 MVP validado! O conceito funciona.")
elif passou >= total * 0.75:
    print("\n  ⚠️  Maioria passou. Busca semântica precisa de API key real.")
else:
    print("\n  🔧 Algo falhou. Veja os detalhes acima.")
print()
