"""Discover agents (.md) and skills (nested .md/.json) under ventura_gold."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from .frontmatter import is_valid_meta, parse_frontmatter

_PKG = Path(__file__).resolve().parent.parent
AGENTS_DIR = _PKG / "agents"
SKILLS_DIR = _PKG / "skills"
ADAPTERS_DIR = _PKG / "adapters"

REQUIRED = ["id", "name", "description", "capabilities", "version", "author"]


def _from_md(path: Path) -> Dict[str, Any] | None:
    try:
        meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        if not is_valid_meta(meta, REQUIRED):
            return None
        if body:
            meta["instructions"] = body
        else:
            meta.setdefault("instructions", "")
        meta["file_path"] = str(path.relative_to(_PKG))
        return meta
    except Exception as e:
        print(f"Warning: failed to load md {path}: {e}")
        return None


def _from_json(path: Path) -> Dict[str, Any] | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not is_valid_meta(data, REQUIRED):
            return None
        data.setdefault("instructions", "")
        data["file_path"] = str(path.relative_to(_PKG))
        return data
    except Exception as e:
        print(f"Warning: failed to load json {path}: {e}")
        return None


def discover_agents() -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    if not AGENTS_DIR.exists():
        return results
    for path in sorted(AGENTS_DIR.rglob("*")):
        if not path.is_file():
            continue
        item = None
        if path.suffix == ".md":
            item = _from_md(path)
        elif path.suffix == ".json":
            item = _from_json(path)
        if item:
            results.append(item)
    return results


def discover_skills() -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    seen_ids: set[str] = set()
    if not SKILLS_DIR.exists():
        return results
    for path in sorted(SKILLS_DIR.rglob("*")):
        if not path.is_file() or path.name == "__init__.py":
            continue
        item = None
        if path.suffix == ".md":
            item = _from_md(path)
        elif path.suffix == ".json":
            item = _from_json(path)
        if item and item["id"] not in seen_ids:
            seen_ids.add(item["id"])
            results.append(item)
    return results


def list_adapters() -> List[str]:
    if not ADAPTERS_DIR.exists():
        return []
    return sorted(p.stem for p in ADAPTERS_DIR.glob("*.py") if p.name != "__init__.py")
