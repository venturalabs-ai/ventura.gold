"""
Validator - project structure and integrity checks.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


def validate_project(root: str | Path | None = None) -> dict[str, Any]:
    """Validate basic project layout and return structured result."""
    root = Path(root) if root else Path.cwd()
    errors: list[dict[str, str]] = []

    required = [
        "src/core/router.py",
        "src/core/runtime.py",
        "src/core/registry.py",
        "src/agents",
        "src/skills",
        "src/adapters",
    ]
    for rel in required:
        if not (root / rel).exists():
            errors.append({"file": rel, "message": f"Missing required path: {rel}"})

    return {"valid": len(errors) == 0, "errors": errors}
