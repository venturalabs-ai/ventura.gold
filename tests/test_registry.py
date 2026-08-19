from ventura_gold.core.registry import discover_agents, discover_skills, list_adapters


def test_discovers_bundled_assets():
    agents = discover_agents()
    skills = discover_skills()
    adapters = list_adapters()
    assert any(a["id"] == "orchestrator" for a in agents)
    assert len(skills) >= 4
    assert "generic" in adapters
