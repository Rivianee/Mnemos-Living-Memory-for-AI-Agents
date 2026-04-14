import click
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from .engine import EvoPalace

@click.group()
@click.version_option()
def cli():
    """Mnemos — Memória que evolui, reorganiza e esquece."""
    pass

@cli.command()
@click.argument("text")
@click.option("--room", "-r", default="general")
@click.option("--importance", "-i", default=0.7, type=float)
def remember(text, room, importance):
    """Salva uma nova memória."""
    palace = EvoPalace("default")
    mem = palace.remember(text, room=room, importance=importance)
    click.echo(f"✅ Memória salva → ID: {mem.id} | Room: {room}")

@cli.command()
@click.argument("query")
@click.option("--top-k", "-k", default=5, type=int)
@click.option("--room", "-r", default=None)
def recall(query, top_k, room):
    """Busca memórias relevantes."""
    palace = EvoPalace("default")
    results = palace.recall(query, top_k=top_k, room_filter=room)
    click.echo(f"🔍 {len(results)} resultado(s) para: '{query}'")
    for i, r in enumerate(results, 1):
        click.echo(f"{i}. [{r['room']}] {r['content'][:100]}")

@cli.command()
def consolidate():
    """Esquece memórias fracas."""
    palace = EvoPalace("default")
    result = palace.consolidate(dry_run=False)
    click.echo(f"💤 Esquecidas: {len(result.get('forgotten', []))} | Restantes: {result.get('kept', 0)}")

@cli.command()
def status():
    """Status do palácio."""
    palace = EvoPalace("default")
    s = palace.status()
    click.echo(f"📊 Memórias: {s['total_memories']} | Rooms: {len(s.get('rooms', {}))} | Links: {s['graph_edges']}")
