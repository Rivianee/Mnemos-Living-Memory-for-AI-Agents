"""
Mnemos — Living Memory Engine
Demo Visual - Roda com: streamlit run app.py
"""

import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from engine import EvoPalace

# ── Config ────────────────────────────────────────────────
st.set_page_config(
    page_title="Mnemos — Living Memory",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: #0a0a0f;
    color: #e8e4d9;
}

.main-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #c8a96e 0%, #e8d5a3 50%, #9b7a3d 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.02em;
}

.subtitle {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: #6b6355;
    letter-spacing: 0.15em;
    text-transform: uppercase;
}

.memory-card, .search-result, .forgotten-card {
    background: #13131a;
    border: 1px solid #2a2518;
    border-radius: 6px;
    padding: 14px 16px;
    margin: 8px 0;
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
}

.memory-card { border-left: 3px solid #c8a96e; }
.memory-card:hover { border-left-color: #e8d5a3; }
.search-result { border-left: 3px solid #4a9a5e; }
.forgotten-card { 
    border-left: 3px solid #6b3333; 
    color: #8a5555;
    text-decoration: line-through;
    opacity: 0.7;
}

.section-header {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #6b6355;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    border-bottom: 1px solid #2a2518;
    padding-bottom: 8px;
    margin: 24px 0 16px 0;
}

.stat-box {
    background: #13131a;
    border: 1px solid #2a2518;
    border-radius: 8px;
    padding: 16px;
    text-align: center;
}

.stat-number {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #c8a96e;
}

.stButton > button {
    background: #1a1812;
    border: 1px solid #c8a96e;
    color: #c8a96e;
}
</style>
""", unsafe_allow_html=True)

# ── Session State ─────────────────────────────────────────
if "palace" not in st.session_state:
    st.session_state.palace = None
if "last_search" not in st.session_state:
    st.session_state.last_search = []
if "last_forgotten" not in st.session_state:
    st.session_state.last_forgotten = []

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="main-title">Mnemos</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Living Memory Engine</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if st.session_state.palace is None:
        # Configuração inicial
        st.markdown('<div class="section-header">Configuration</div>', unsafe_allow_html=True)

        api_key = st.text_input("Google API Key", type="password", placeholder="AIza...", key="api_key")
        palace_name = st.text_input("Palace Name", value="my_palace", key="palace_name")
        forget_threshold = st.slider("Forget Threshold", 0.05, 0.5, 0.15, 0.05,
            help="Memórias abaixo desse score são esquecidas", key="forget_threshold")

        if st.button("⚡ Initialize Palace", use_container_width=True, key="init_palace"):
            with st.spinner("Building palace..."):
                st.session_state.palace = EvoPalace(
                    palace_name=palace_name,
                    api_key=api_key if api_key else None,
                    persist_path=f"./demo_data_{palace_name}",
                    forget_threshold=forget_threshold,
                )
                st.session_state.last_search = []
                st.session_state.last_forgotten = []
            st.success("✅ Palace initialized!")
            st.rerun()

    else:
        # Quick Actions (depois de inicializado)
        st.markdown('<div class="section-header">Quick Actions</div>', unsafe_allow_html=True)

        if st.button("🚀 Load Demo Memories (15)", use_container_width=True, key="load_demo"):
            with st.spinner("Carregando demonstração..."):
                st.session_state.palace.load_demo_memories(15)
            st.success("✅ Demo carregada!")
            st.rerun()

        if st.button("🧹 Consolidate All Now", use_container_width=True, key="consolidate_now"):
            with st.spinner("Consolidando..."):
                result = st.session_state.palace.consolidate(dry_run=False)
            st.success(f"Esquecidas: {len(result.get('forgotten', []))}")
            st.rerun()

        # Stats
        st.markdown('<div class="section-header">Palace Stats</div>', unsafe_allow_html=True)
        s = st.session_state.palace.status()
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Memories", s["total_memories"])
        with c2:
            st.metric("Links", s["graph_edges"])

        st.markdown('<div class="section-header">Rooms</div>', unsafe_allow_html=True)
        for room, count in s.get("rooms", {}).items():
            st.write(f"{room} → **{count}**")

# ── Main Area ─────────────────────────────────────────────
if st.session_state.palace is None:
    st.markdown('<br><br><br>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center"><div class="main-title" style="font-size:4.5rem">Mnemos</div></div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center"><div class="subtitle" style="font-size:1rem">Memory that evolves. Learns. Forgets.</div></div>', unsafe_allow_html=True)
    st.stop()

palace = st.session_state.palace

tab1, tab2, tab3, tab4, tab5 = st.tabs(["💾 Remember", "🔍 Recall", "↺ Reorganize", "💤 Consolidate", "🗺️ Palace Map"])

# Tab 1: Remember
with tab1:
    st.markdown('<div class="section-header">Store a Memory</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        content = st.text_area("Memory content", placeholder="What should I remember?", height=120)
    with col2:
        room = st.text_input("Room", value="general", key="room_input")
        tags_raw = st.text_input("Tags (comma separated)", placeholder="tag1, tag2", key="tags_input")
        importance = st.slider("Importance", 0.1, 1.0, 0.7, 0.05, key="imp_slider")

    if st.button("💾 Store Memory", use_container_width=True, key="store_btn"):
        if content.strip():
            tags = [t.strip() for t in tags_raw.split(",") if t.strip()]
            mem = palace.remember(content, room=room, tags=tags, importance=importance)
            st.success(f"Memory `{mem.id}` saved in `{room}`")
            st.rerun()
        else:
            st.warning("Content cannot be empty.")

    st.markdown('<div class="section-header">All Memories</div>', unsafe_allow_html=True)
    memories = palace.list_all()
    for m in memories:
        bar_width = int(m["importance"] * 100)
        st.markdown(f"""
        <div class="memory-card">
            <div class="room-tag">{m['room']} · id:{m['id']} · accessed {m['access_count']}x</div>
            <div class="content">{m['content']}</div>
            <div class="importance-bar" style="width:{bar_width}%"></div>
        </div>
        """, unsafe_allow_html=True)

# Tab 2: Recall
with tab2:
    st.markdown('<div class="section-header">Semantic Search</div>', unsafe_allow_html=True)
    query = st.text_input("What do you want to remember?", placeholder="how does the user like to be answered?")
    col1, col2 = st.columns([1, 2])
    with col1:
        top_k = st.slider("Results", 1, 10, 3)
    with col2:
        room_filter = st.text_input("Filter by room (optional)", placeholder="usuario/preferencias")

    if st.button("🔍 Search Memory", use_container_width=True):
        if query.strip():
            with st.spinner("Searching the palace..."):
                results = palace.recall(query, top_k=top_k, room_filter=room_filter or None)
            st.session_state.last_search = results

    if st.session_state.last_search:
        st.markdown(f'<div class="section-header">{len(st.session_state.last_search)} results found</div>', unsafe_allow_html=True)
        for r in st.session_state.last_search:
            st.markdown(f"""
            <div class="search-result">
                <div class="match-score">room:{r['room']} · id:{r['id']} · distance:{r['distance']} · importance:{r['importance']}</div>
                <div class="content">{r['content']}</div>
            </div>
            """, unsafe_allow_html=True)

# Tab 3: Reorganize
with tab3:
    st.markdown('<div class="section-header">Dynamic Reorganization</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-family:Space Mono,monospace;font-size:0.78rem;color:#6b6355;margin-bottom:16px">PageRank redistributes importance based on memory connections and access patterns.</div>', unsafe_allow_html=True)

    if st.button("↺ Reorganize Palace", use_container_width=True):
        with st.spinner("Running PageRank..."):
            changes = palace.reorganize()
        if changes:
            st.success(f"{len(changes)} memories updated")
            for mem_id, diff in changes.items():
                direction = "↑" if diff["new"] > diff["old"] else "↓"
                color = "#4a9a5e" if diff["new"] > diff["old"] else "#9a4a4a"
                st.markdown(f'<div style="font-family:Space Mono,monospace;font-size:0.75rem;padding:4px 0"><span style="color:#6b6355">[{mem_id}]</span> {diff["old"]} <span style="color:{color}">{direction} {diff["new"]}</span></div>', unsafe_allow_html=True)
        else:
            st.info("No significant changes.")

    # Link Memories
    st.markdown('<div class="section-header">Link Memories</div>', unsafe_allow_html=True)
    memories = palace.list_all()
    ids = [m["id"] for m in memories]
    if len(ids) >= 2:
        c1, c2, c3 = st.columns(3)
        with c1: id_a = st.selectbox("From", ids, key="link_from")
        with c2: id_b = st.selectbox("To", [i for i in ids if i != id_a], key="link_to")
        with c3: relation = st.text_input("Relation", value="related", key="link_relation")
        if st.button("🔗 Create Link", use_container_width=True):
            palace.link(id_a, id_b, relation=relation)
            st.success(f"Linked {id_a} → {id_b}")
            st.rerun()

# Tab 4 e Tab 5 estão cortadas aqui por limite de tamanho, mas o importante é que o botão Load Demo e a Tab 5 agora devem aparecer.

# ── Tab 4: Consolidate ────────────────────────────────────
with tab4:
    st.markdown('<div class="section-header">💤 Memory Consolidation</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-family:Space Mono,monospace;font-size:0.78rem;color:#6b6355;margin-bottom:16px">Aplica a curva de esquecimento de Ebbinghaus. Memórias fracas (pouco acessadas + baixa importância) são removidas automaticamente. Memórias importantes resistem.</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔍 Preview (Dry Run)", use_container_width=True):
            result = palace.consolidate(dry_run=True)
            st.session_state.last_forgotten = result["forgotten"]
            if result["forgotten"]:
                st.warning(f"{len(result['forgotten'])} memórias seriam esquecidas")
            else:
                st.success("Todas as memórias estão saudáveis.")

    with col2:
        if st.button("💤 Consolidate Now", use_container_width=True):
            result = palace.consolidate(dry_run=False)
            st.session_state.last_forgotten = result["forgotten"]
            if result["forgotten"]:
                st.success(f"Esqueceu {len(result['forgotten'])} memórias fracas. {result['kept']} permanecem.")
            else:
                st.info("Nada para esquecer no momento.")
            st.rerun()

    with col3:
        if st.button("🔬 Simular Conversa Longa (50 msgs)", use_container_width=True):
            with st.spinner("Simulando 50 mensagens + consolidação..."):
                for i in range(50):
                    fake_content = f"Mensagem {i+1} da conversa longa sobre o projeto Mnemos, preferências do usuário e testes de memória dinâmica."
                    palace.remember(fake_content, room="conversa/long_test", importance=0.65 if i % 4 == 0 else 0.25)
                result = palace.consolidate(dry_run=False)
            st.success(f"✅ Simulação concluída! Esquecidas: {len(result.get('forgotten', []))} | Restantes: {result.get('kept', 0)}")
            st.rerun()

    # Mostrar memórias esquecidas
    if st.session_state.last_forgotten:
        st.markdown('<div class="section-header">Memórias Esquecidas</div>', unsafe_allow_html=True)
        for mem_id, score in st.session_state.last_forgotten[:10]:  # limita para não poluir
            st.markdown(f'<div class="forgotten-card">[{mem_id}] forgetting score: {score}</div>', unsafe_allow_html=True)

    # Health das memórias restantes
    st.markdown('<div class="section-header">Memory Health (Atual)</div>', unsafe_allow_html=True)
    memories = palace.list_all()
    for m in memories[:15]:  # mostra só as primeiras 15 para não ficar gigante
        score = m["forgetting_score"]
        color = "#4a9a5e" if score > 0.5 else "#9a8a3a" if score > 0.25 else "#9a4a4a"
        bar = int(score * 100)
        st.markdown(f"""
        <div style="margin:8px 0;font-family:Space Mono,monospace;font-size:0.75rem">
            <span style="color:#6b6355">[{m['id']}]</span> 
            <span style="color:#d4cfc4;margin:0 8px">{m['content'][:55]}...</span>
            <span style="color:{color}">score: {score}</span>
        </div>
        <div style="height:3px;width:{bar}%;background:{color};border-radius:2px;margin-bottom:10px;opacity:0.75"></div>
        """, unsafe_allow_html=True)

    if len(memories) > 15:
        st.caption(f"... e mais {len(memories)-15} memórias")

# ── Tab 5: Palace Map ─────────────────────────────────────
with tab5:
    st.markdown('<div class="section-header">🗺️ Palace Map — Visão Geral do Palácio</div>', unsafe_allow_html=True)
    map_data = palace.get_palace_map()
    
    st.metric("Total Memories", map_data["total_memories"])
    st.metric("Total Rooms", map_data["total_rooms"])
    st.metric("Graph Edges", map_data["graph_edges"])

    st.markdown("### Rooms e Centralidade")
    for room_name, data in sorted(map_data["rooms"].items(), key=lambda x: x[1]["centrality"], reverse=True):
        centrality = round(data["centrality"] * 100, 1)
        color = "#c8a96e" if centrality > 50 else "#9b7a3d"
        st.markdown(f"""
        <div class="memory-card">
            <div class="room-tag">{room_name} <span style="color:{color}">({centrality}% central)</span></div>
            <div style="color:#d4cfc4">Memórias: {data["count"]}</div>
        </div>
        """, unsafe_allow_html=True)