"""Runtime tests"""
import pytest
from core.runtime import run


def test_rejects_empty_prompt():
    with pytest.raises(ValueError, match="vazio"):
        run("")


def test_builds_plan_without_provider():
    agents = [{"id": "a", "name": "A", "description": "desc", "capabilities": ["x"], "instructions": "Instrução base"}]
    result = run("Olá mundo", agents, [])
    assert result["providerResponse"] is None
    assert "Olá mundo" in result["instructions"]
    assert result["plan"]["selectedAgent"]["id"] == "a"
