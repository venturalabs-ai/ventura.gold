from ventura_gold.core.router import normalize_text, route


def test_normalize():
    assert "acao" in normalize_text("Ação")


def test_route():
    agents = [
        {"id": "orchestrator", "name": "Orquestrador", "description": "geral", "capabilities": ["coord"]},
        {"id": "repo", "name": "Analista de Repositório", "description": "scan git", "capabilities": ["repositório", "scan"]},
    ]
    r = route("analisar repositório scan", agents, [])
    assert r["agent"]["id"] in ("repo", "orchestrator")
