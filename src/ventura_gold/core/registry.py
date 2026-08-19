"""Discover agents and skills from JSON definitions."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

_PKG = Path(__file__).resolve().parent.parent
AGENTS_DIR = _PKG / "agents"
SKILLS_DIR = _PKG / "skills"
ADAPTERS_DIR = _PKG / "adapters"


def _load_json_dir(directory: Path, kind: str) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    if not directory.exists():
        return results
    for path in sorted(directory.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            required = ["id", "name", "description", "capabilities", "version", "author"]
            if all(data.get(f) for f in required):
                data.setdefault("instructions", "")
                data["file_path"] = path.name
                results.append(data)
        except Exception as e:
            print(f"Warning: failed to load {kind} {path}: {e}")
    return results


def discover_agents() -> List[Dict[str, Any]]:
    return _load_json_dir(AGENTS_DIR, "agent")


def discover_skills() -> List[Dict[str, Any]]:
    return _load_json_dir(SKILLS_DIR, "skill")


def list_adapters() -> List[str]:
    if not ADAPTERS_DIR.exists():
        return []
    return sorted(p.stem for p in ADAPTERS_DIR.glob("*.py") if p.name != "__init__.py")
