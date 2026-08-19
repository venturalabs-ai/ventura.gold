"""Frontmatter tests"""
from core.frontmatter import parse_frontmatter, is_valid_frontmatter


def test_parse_valid():
    content = "---\nid: a\nname: A\n---\nCorpo"
    meta = parse_frontmatter(content)
    assert meta is not None
    assert meta["id"] == "a"
    assert meta["name"] == "A"


def test_required_fields():
    assert is_valid_frontmatter({"id": "x", "name": "N"}, ["id", "name"]) is True
    assert is_valid_frontmatter({"id": "x"}, ["id", "name"]) is False
