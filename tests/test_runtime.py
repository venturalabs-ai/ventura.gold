import pytest
from ventura_gold.core.runtime import run_prompt


def test_empty_prompt():
    with pytest.raises(ValueError):
        run_prompt("")


def test_local_mode(tmp_path):
    result = run_prompt("olá", tmp_path, provider="generic")
    assert result["mode"] == "local"
    assert "olá" in result["instructions"].lower() or "olá" in result["instructions"]
