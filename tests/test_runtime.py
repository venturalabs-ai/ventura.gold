import pytest
from ventura_gold.core.runtime import run_prompt


def test_empty_prompt():
    with pytest.raises(ValueError):
        run_prompt("")


def test_local_run():
    result = run_prompt("ola", provider="generic")
    assert result["mode"] == "local"
    assert "ola" in result["instructions"]
