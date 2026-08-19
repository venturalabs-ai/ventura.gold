"""Project validation."""
from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Tuple

from .registry import discover_agents, discover_skills, list_adapters


def validate_all(root: Optional[Path] = None) -> Tuple[List[str], List[str]]:
    root = (root or Path.cwd()).resolve()
    errors: List[str] = []
    warnings: List[str] = []

    agents = discover_agents()
    skills = discover_skills()
    adapters = list_adapters()
    if not agents:
        errors.append("Nenhum agente válido encontrado em ventura_gold/agents")
    if not skills:
        warnings.append("Nenhuma skill JSON encontrada")
    if len(adapters) < 5:
        warnings.append(f"Poucos adaptadores: {len(adapters)}")
    return errors, warnings


def validate_project(root: Optional[Path] = None) -> dict:
    errors, warnings = validate_all(root)
    return {
        "valid": len(errors) == 0,
        "errors": [{"file": "project", "message": e} for e in errors],
        "warnings": warnings,
    }
