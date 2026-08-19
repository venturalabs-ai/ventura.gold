from ventura_gold.core.registry import discover_agents, discover_skills, list_adapters


def test_discovers_bundled_assets():
    agents = discover_agents()
    skills = discover_skills()
    adapters = list_adapters()
    assert any(a["id"] == "orchestrator" for a in agents)
    assert any(a.get("file_path", "").endswith(".md") for a in agents)
    ids = {s["id"] for s in skills}
    assert "repository" in ids
    assert "codegen" in ids
    assert "testing" in ids
    assert "docs" in ids
    assert "review" in ids
    assert len(skills) >= 5
    assert "generic" in adapters
