from ventura_gold.core.router import normalize_text, route


def test_normalize():
    assert "acao" in normalize_text("Acao") or "acao" in normalize_text("Acao")


def test_route_repo():
    agents = [
        {"id": "orchestrator", "name": "Orquestrador", "description": "geral", "capabilities": ["coord"]},
        {"id": "repo", "name": "Analista de Repositorio", "description": "scan git", "capabilities": ["repositorio", "scan"]},
    ]
    r = route("fazer scan do repositorio", agents, [])
    assert r["agent"]["id"] == "repo"
