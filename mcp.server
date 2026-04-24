"""
EvoPalace Engine — Memória viva para agentes de IA
Diferencial: memória que evolui, esquece e se reorganiza como um cérebro

Estrutura:
  Wing (ala) → Hall (corredor) → Room (quarto) → Memory (memória)

Requer: pip install chromadb networkx google-generativeai pyyaml
"""

import os
import math
import time
import json
import uuid
import hashlib
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Optional

import chromadb
import networkx as nx
import yaml


# ─── Modelos ──────────────────────────────────────────────────────────────────

@dataclass
class Memory:
    id: str
    content: str
    room: str           # ex: "work/projects/evopalace"
    tags: list[str]
    created_at: float
    last_accessed: float
    access_count: int
    importance: float   # 0.0 → 1.0 — dinâmico
    embedding: list[float] = field(default_factory=list, repr=False)


@dataclass
class Room:
    path: str           # ex: "work/projects/evopalace"
    memory_count: int = 0
    centrality: float = 0.0  # posição no grafo (quanto mais central, mais importante)


# ─── Curva de Esquecimento (Ebbinghaus) ───────────────────────────────────────

def forgetting_score(last_accessed: float, access_count: int, base_importance: float) -> float:
    """
    Quanto mais tempo sem acessar e menos vezes acessada → menor o score.
    Memórias muito acessadas resistem ao esquecimento.
    """
    hours_since = (time.time() - last_accessed) / 3600
    decay = 0.1  # constante de esquecimento
    retention = math.exp(-decay * hours_since)
    boost = min(access_count * 0.05, 0.5)  # acesso frequente aumenta até +0.5
    return min(1.0, base_importance * retention + boost)


# ─── Embeddings ───────────────────────────────────────────────────────────────

def get_embedding(text: str, api_key: Optional[str] = None) -> list[float]:
    """
    Retorna embedding real (Google) ou simulado (modo offline).
    """
    if api_key:
        try:
            import requests
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:embedContent?key={api_key}"
            body = {"model": "models/gemini-embedding-001", "content": {"parts": [{"text": text}]}}
            r = requests.post(url, json=body, timeout=10)
            if not r.ok:
                print(f"[DEBUG API] {r.status_code}: {r.text[:300]}")
            r.raise_for_status()
            return r.json()["embedding"]["values"]
        except Exception as e:
            print(f"[WARN] Embedding API falhou, usando modo offline: {e}")

    # Modo offline: hash determinístico → vetor de 128 dims
    h = hashlib.sha256(text.encode()).digest()
    vec = [(b / 255.0) * 2 - 1 for b in h]  # 32 valores em [-1, 1]
    # Expande para 128
    vec = (vec * 4)[:128]
    # Normaliza
    norm = math.sqrt(sum(x**2 for x in vec)) or 1
    return [x / norm for x in vec]


# ─── Engine Principal ──────────────────────────────────────────────────────────

class EvoPalace:
    def __init__(
        self,
        palace_name: str = "MyPalace",
        api_key: Optional[str] = None,
        persist_path: str = "./evopalace_data",
        forget_threshold: float = 0.15,  # memórias abaixo disso são esquecidas
    ):
        self.palace_name = palace_name
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.forget_threshold = forget_threshold
        self.persist_path = persist_path

        os.makedirs(persist_path, exist_ok=True)

        # ChromaDB — armazena memórias com embeddings
        self._chroma = chromadb.PersistentClient(path=persist_path)
        self._col = self._chroma.get_or_create_collection(
            name=palace_name,
            embedding_function=None  # gerenciamos os embeddings manualmente
        )

        # NetworkX — grafo de relações entre memórias
        self._graph = nx.DiGraph()
        self._graph_path = os.path.join(persist_path, "graph.json")
        self._load_graph()

        # Metadados das memórias (importância, acessos, etc.)
        self._meta_path = os.path.join(persist_path, "meta.yaml")
        self._meta: dict[str, dict] = self._load_meta()

        mode = "🟢 com Google Gemini" if self.api_key else "🟡 modo offline (sem API key)"
        print(f"[EvoPalace] '{palace_name}' iniciado {mode}")
        print(f"[EvoPalace] {len(self._meta)} memórias carregadas")

    # ── Salvar ─────────────────────────────────────────────────────────────────

    def remember(
        self,
        content: str,
        room: str = "general",
        tags: list[str] = None,
        importance: float = 0.7,
    ) -> Memory:
        """Grava uma nova memória no palácio."""
        tags = tags or []
        mem_id = str(uuid.uuid4())[:8]
        now = time.time()

        embedding = get_embedding(content, self.api_key)

        mem = Memory(
            id=mem_id,
            content=content,
            room=room,
            tags=tags,
            created_at=now,
            last_accessed=now,
            access_count=1,
            importance=importance,
            embedding=embedding,
        )

        # Salva no ChromaDB
        self._col.add(
            ids=[mem_id],
            embeddings=[embedding],
            documents=[content],
            metadatas=[{"room": room, "tags": json.dumps(tags), "importance": importance}],
        )

        # Salva metadados
        self._meta[mem_id] = {
            "room": room,
            "tags": tags,
            "created_at": now,
            "last_accessed": now,
            "access_count": 1,
            "importance": importance,
        }
        self._save_meta()

        # Adiciona nó no grafo
        self._graph.add_node(mem_id, room=room, importance=importance)
        self._save_graph()

        # Cria arestas com memórias do mesmo quarto (co-localização)
        same_room = [m for m, d in self._meta.items() if d["room"] == room and m != mem_id]
        for other_id in same_room[-3:]:  # conecta com as 3 últimas do mesmo quarto
            self._graph.add_edge(mem_id, other_id, weight=0.5, relation="co_room")
        self._save_graph()

        print(f"[+] Memória '{mem_id}' salva em room='{room}'")
        return mem

    # ── Buscar ─────────────────────────────────────────────────────────────────

    def recall(
        self,
        query: str,
        top_k: int = 5,
        room_filter: Optional[str] = None,
    ) -> list[dict]:
        """Busca memórias relevantes. Atualiza acesso e importância."""
        query_emb = get_embedding(query, self.api_key)

        where = {"room": room_filter} if room_filter else None

        results = self._col.query(
            query_embeddings=[query_emb],
            n_results=min(top_k, self._col.count()),
            where=where,
        )

        if not results["ids"][0]:
            return []

        memories = []
        for i, mem_id in enumerate(results["ids"][0]):
            meta = self._meta.get(mem_id, {})

            # Atualiza acesso
            meta["access_count"] = meta.get("access_count", 0) + 1
            meta["last_accessed"] = time.time()
            self._meta[mem_id] = meta

            # Aumenta peso das arestas no grafo (memória mais acessada fica mais central)
            if self._graph.has_node(mem_id):
                self._graph.nodes[mem_id]["importance"] = min(
                    1.0, meta["importance"] + 0.02
                )

            memories.append({
                "id": mem_id,
                "content": results["documents"][0][i],
                "room": meta.get("room", "?"),
                "tags": meta.get("tags", []),
                "importance": meta.get("importance", 0.5),
                "access_count": meta.get("access_count", 1),
                "distance": round(results["distances"][0][i], 4),
            })

        self._save_meta()
        self._save_graph()
        return memories

    # ── Conectar memórias manualmente ─────────────────────────────────────────

    def link(self, id_a: str, id_b: str, relation: str = "related", weight: float = 0.8):
        """Cria uma relação explícita entre duas memórias."""
        if id_a not in self._meta or id_b not in self._meta:
            print("[WARN] Um dos IDs não existe")
            return
        self._graph.add_edge(id_a, id_b, weight=weight, relation=relation)
        self._save_graph()
        print(f"[~] Ligação criada: {id_a} → {id_b} ({relation})")

    # ── Reorganizar (grafo dinâmico) ──────────────────────────────────────────

    def reorganize(self) -> dict:
        """
        Recalcula centralidade do grafo.
        Memórias mais conectadas e acessadas sobem de importância.
        """
        if len(self._graph.nodes) < 2:
            print("[~] Grafo pequeno demais para reorganizar")
            return {}

        centrality = nx.pagerank(self._graph, weight="weight")

        changes = {}
        for mem_id, score in centrality.items():
            if mem_id in self._meta:
                old = self._meta[mem_id]["importance"]
                # Combina centralidade do grafo com histórico de acesso
                access_boost = min(self._meta[mem_id].get("access_count", 1) * 0.02, 0.3)
                new_importance = min(1.0, score * 2 + access_boost)
                self._meta[mem_id]["importance"] = round(new_importance, 3)
                if abs(new_importance - old) > 0.01:
                    changes[mem_id] = {"old": round(old, 3), "new": round(new_importance, 3)}

        self._save_meta()
        print(f"[↺] Reorganizado: {len(changes)} memórias atualizaram importância")
        return changes

    # ── Esquecer (curva de Ebbinghaus) ────────────────────────────────────────

    def consolidate(self, dry_run: bool = False) -> dict:
        """
        Aplica curva de esquecimento.
        Memórias fracas são removidas. Memórias fortes sobrevivem.
        dry_run=True: só mostra o que seria esquecido, não apaga.
        """
        to_forget = []
        to_keep = []

        for mem_id, meta in self._meta.items():
            score = forgetting_score(
                last_accessed=meta.get("last_accessed", time.time()),
                access_count=meta.get("access_count", 1),
                base_importance=meta.get("importance", 0.5),
            )
            if score < self.forget_threshold:
                to_forget.append((mem_id, round(score, 3)))
            else:
                to_keep.append((mem_id, round(score, 3)))

        if not dry_run and to_forget:
            ids_to_remove = [m[0] for m in to_forget]
            self._col.delete(ids=ids_to_remove)
            for mem_id in ids_to_remove:
                del self._meta[mem_id]
                if self._graph.has_node(mem_id):
                    self._graph.remove_node(mem_id)
            self._save_meta()
            self._save_graph()

        result = {
            "forgotten": to_forget,
            "kept": len(to_keep),
            "dry_run": dry_run,
        }
        action = "seria esquecido" if dry_run else "esquecido"
        print(f"[💤] Consolidação: {len(to_forget)} {action}, {len(to_keep)} mantido(s)")
        return result

    # ── Inspecionar ───────────────────────────────────────────────────────────

    def status(self) -> dict:
        """Retorna estado atual do palácio."""
        rooms = {}
        for meta in self._meta.values():
            r = meta.get("room", "?")
            rooms[r] = rooms.get(r, 0) + 1

        top_memories = sorted(
            self._meta.items(),
            key=lambda x: x[1].get("importance", 0),
            reverse=True
        )[:5]

        return {
            "palace": self.palace_name,
            "total_memories": len(self._meta),
            "rooms": rooms,
            "graph_nodes": self._graph.number_of_nodes(),
            "graph_edges": self._graph.number_of_edges(),
            "top_memories": [
                {"id": m[0], "room": m[1]["room"], "importance": m[1]["importance"]}
                for m in top_memories
            ],
        }

    def list_all(self) -> list[dict]:
        """Lista todas as memórias com seus metadados."""
        all_mems = []
        for mem_id, meta in self._meta.items():
            try:
                doc = self._col.get(ids=[mem_id])
                content = doc["documents"][0] if doc["documents"] else "?"
            except Exception:
                content = "?"
            all_mems.append({
                "id": mem_id,
                "content": content[:80] + "..." if len(content) > 80 else content,
                "room": meta.get("room", "?"),
                "importance": meta.get("importance", 0.5),
                "access_count": meta.get("access_count", 1),
                "forgetting_score": round(forgetting_score(
                    meta.get("last_accessed", time.time()),
                    meta.get("access_count", 1),
                    meta.get("importance", 0.5),
                ), 3),
            })
        return sorted(all_mems, key=lambda x: x["importance"], reverse=True)

    # ── Persistência ──────────────────────────────────────────────────────────

    def load_demo_memories(self, count: int = 15):
        """Carrega memórias de demonstração variadas para testes rápidos."""
        demo_data = [
            ("Riviane prefere respostas diretas, curtas, sem enrolação e com emojis moderados", "usuario/preferencias", 0.95),
            ("O projeto se chama Mnemos e é uma memória viva que reorganiza e esquece sozinha", "projeto/objetivo", 0.93),
            ("Nunca commitar sem rodar os testes primeiro", "projeto/regras", 0.90),
            ("Lembrar de comprar café amanhã", "pessoal/tarefas", 0.15),
            ("Milla Jovovich lançou MemPalace em 05/04/2026 e viralizou com ~40k stars", "contexto/ia", 0.80),
            ("Eu gosto de projetos que combinam memória dinâmica com visualização bonita", "usuario/gostos", 0.85),
            ("Em conversas longas, rodar consolidação a cada 30-50 interações ajuda muito", "projeto/dicas", 0.88),
            ("Teste de contexto longo: o palácio deve manter preferências mesmo após muitas mensagens", "teste/limite", 0.82),
            ("Skill viva básica será adicionada na próxima fase", "roadmap/skills", 0.70),
            # Adicione mais se quiser
        ][:count]
        for content, room, imp in demo_data:
            self.remember(content, room=room, importance=imp)
        print(f"[DEMO] {len(demo_data)} memórias carregadas com sucesso!")

    def get_palace_map(self) -> dict:
        """Dados para visualização do palácio (rooms + centralidade)."""
        rooms = {}
        for mem_id, meta in self._meta.items():
            room = meta.get("room", "general")
            if room not in rooms:
                rooms[room] = {"count": 0, "centrality": 0.0, "memories": []}
            rooms[room]["count"] += 1
            rooms[room]["memories"].append({
                "id": mem_id,
                "importance": meta.get("importance", 0.5),
                "access_count": meta.get("access_count", 1)
            })

        if self._graph.number_of_nodes() > 0:
            try:
                centrality = nx.pagerank(self._graph, weight="weight")
                for mem_id, score in centrality.items():
                    if mem_id in self._meta:
                        room = self._meta[mem_id].get("room")
                        if room in rooms:
                            rooms[room]["centrality"] = max(rooms[room]["centrality"], score)
            except:
                pass

        return {
            "rooms": rooms,
            "total_rooms": len(rooms),
            "total_memories": len(self._meta),
            "graph_nodes": self._graph.number_of_nodes(),
            "graph_edges": self._graph.number_of_edges()
        }
    
    def _load_meta(self) -> dict:
        if os.path.exists(self._meta_path):
            with open(self._meta_path, "r") as f:
                return yaml.safe_load(f) or {}
        return {}

    def _save_meta(self):
        with open(self._meta_path, "w") as f:
            yaml.dump(self._meta, f)

    def _load_graph(self):
        if os.path.exists(self._graph_path):
            with open(self._graph_path, "r") as f:
                data = json.load(f)
            self._graph = nx.node_link_graph(data)

    def _save_graph(self):
        with open(self._graph_path, "w") as f:
            json.dump(nx.node_link_data(self._graph), f)
