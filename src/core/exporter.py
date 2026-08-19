"""
Exporter - Generate portable agent package JSON.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def export_package(
    agents: list[dict[str, Any]],
    skills: list[dict[str, Any]],
    adapters: list[str],
    root_dir: str | Path,
) -> dict[str, Any]:
    """Write dist/ventura-agent-package.json and return path + package."""
    root = Path(root_dir)
    pkg = {
        "format": "ventura-agent-package/v1",
        "name": "ventura.gold",
        "version": "1.0.0",
        "authentication": "none-for-local-runtime",
        "portability": adapters,
        "agents": [
            {
                "id": a.get("id"),
                "name": a.get("name"),
                "description": a.get("description"),
                "capabilities": a.get("capabilities", []),
                "version": a.get("version"),
                "author": a.get("author"),
            }
            for a in agents
        ],
        "skills": [
            {
                "id": s.get("id"),
                "name": s.get("name"),
                "description": s.get("description"),
                "capabilities": s.get("capabilities", []),
                "version": s.get("version"),
                "author": s.get("author"),
            }
            for s in skills
        ],
        "adapters": adapters,
    }

    out_dir = root / "dist"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "ventura-agent-package.json"
    out_path.write_text(json.dumps(pkg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {"path": str(out_path), "package": pkg}
