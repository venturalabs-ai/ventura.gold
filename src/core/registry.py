"""
Agent Registry - Discovers and registers agents and skills from JSON files.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_CORE_DIR = Path(__file__).resolve().parent
AGENTS_DIR = _CORE_DIR.parent / "agents"
SKILLS_DIR = _CORE_DIR.parent / "skills"


def discover_agents() -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    if not AGENTS_DIR.exists():
        print(f"Warning: Agents directory not found: {AGENTS_DIR}")
        return results

    for filepath in sorted(AGENTS_DIR.glob("*.json")):
        try:
            data = json.loads(filepath.read_text(encoding="utf-8"))
            required = ["id", "name", "description", "capabilities", "version", "author"]
            if all(field in data and data[field] for field in required):
                results.append(
                    {
                        "file_path": f"src/agents/{filepath.name}",
                        "id": data["id"],
                        "name": data["name"],
                        "description": data["description"],
                        "capabilities": data.get("capabilities", []),
                        "version": data.get("version", "0.1.0"),
                        "author": data.get("author", "Unknown"),
                        "instructions": data.get("instructions", ""),
                    }
                )
            else:
                print(f"Warning: Invalid agent metadata in: {filepath}")
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
    return results


def discover_skills() -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    if not SKILLS_DIR.exists():
        print(f"Warning: Skills directory not found: {SKILLS_DIR}")
        return results

    for filepath in sorted(SKILLS_DIR.glob("*.json")):
        try:
            data = json.loads(filepath.read_text(encoding="utf-8"))
            required = ["id", "name", "description", "capabilities", "version", "author"]
            if all(field in data and data[field] for field in required):
                results.append(
                    {
                        "file_path": f"src/skills/{filepath.name}",
                        "id": data["id"],
                        "name": data["name"],
                        "description": data["description"],
                        "capabilities": data.get("capabilities", []),
                        "version": data.get("version", "0.1.0"),
                        "author": data.get("author", "Unknown"),
                        "instructions": data.get("instructions", ""),
                    }
                )
            else:
                print(f"Warning: Invalid skill metadata in: {filepath}")
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
    return results


def validate_agent(agent: dict) -> dict[str, Any]:
    errors = []
    required = ["id", "name", "description", "capabilities", "version", "author"]
    for field in required:
        if field not in agent or not agent[field]:
            errors.append(f"Missing `{field}` field")
    return {"valid": len(errors) == 0, "errors": errors}


def validate_skill(skill: dict) -> dict[str, Any]:
    return validate_agent(skill)
