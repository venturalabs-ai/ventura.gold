"""Router tests"""
from core.router import route, score_candidate, normalize_text


def test_normalize_removes_accents():
    assert "acao" in normalize_text("Ação")


def test_route_selects_by_name():
    agents = [
        {"id": "marketing", "name": "Especialista em Marketing", "description": "Campanhas", "capabilities": ["marketing", "campanha"]},
        {"id": "orchestrator", "name": "Orquestrador", "description": "Geral", "capabilities": ["coordenacao"]},
    ]
    result = route("planejar campanha de marketing", agents, [])
    assert result["agent"]["id"] == "marketing"


def test_fallback_orchestrator():
    agents = [
        {"id": "marketing", "name": "Marketing", "description": "x", "capabilities": ["mkt"]},
        {"id": "orchestrator", "name": "Orquestrador", "description": "geral", "capabilities": ["coord"]},
    ]
    result = route("xyzabc sem match", agents, [])
    assert result["agent"]["id"] == "orchestrator"
