"""Validator tests"""
from core.validator import validate_project


def test_validate_structure():
    result = validate_project()
    assert "valid" in result
    assert "errors" in result
    assert isinstance(result["valid"], bool)
    assert isinstance(result["errors"], list)
