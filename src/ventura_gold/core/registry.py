"""Registry — descoberta de agentes e skills (JSON ou Markdown)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, List

_PKG = Path(__file__).resolve().parent.parent
AGENTS_DIR = _PKG / "agents"
SKILLS_DIR = _PKG / "skills"


def _load_json_dir(directory: Path, kind: str) -> List[dict[str, Any]]:
    results: List[dict[str, Any]] = []
    if not directory.exists():
        return results
    for path in sorted(directory.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            required = ["id", "name", "description"]
            if all(data.get(f) for f in required):
                results.append(
                    {
                        "id": data["id"],
                        "name": data["name"],
                        "description": data["description"],
                        "capabilities": data.get("capabilities", []),
                        "version": data.get("version", "1.0.0"),
                        "author": data.get("author", "Ventura Labs AI"),
                        "instructions": data.get("instructions", data.get("description", "")),
                    }
                )
        except Exception as e:
            print(f"Warning: failed to load {path}: {e}")
    return results


def discover_agents(root: Path | None = None) -> List[dict[str, Any]]:
    directory = (root / "src" / "ventura_gold" / "agents") if root else AGENTS_DIR
    if root and not directory.exists():
        directory = root / "src" / "agents"
    if not directory.exists():
        directory = AGENTS_DIR
    return _load_json_dir(directory, "agent")


def discover_skills(root: Path | None = None) -> List[dict[str, Any]]:
    directory = (root / "src" / "ventura_gold" / "skills") if root else SKILLS_DIR
    json_dir = directory if directory.exists() else AGENTS_DIR.parent / "skills"
    results = _load_json_dir(json_dir, "skill")
    if not results and (AGENTS_DIR.parent / "skills").exists():
        results = _load_json_dir(AGENTS_DIR.parent / "skills", "skill")
    return results


def list_adapters() -> List[str]:
    adapters_dir = _PKG / "adapters"
    if not adapters_dir.exists():
        return []
    return sorted(p.stem for p in adapters_dir.glob("*.py") if p.name != "__init__.py")
