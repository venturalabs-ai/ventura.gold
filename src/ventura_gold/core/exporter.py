"""Export portable package."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

from .registry import discover_agents, discover_skills, list_adapters


def export_package(root: Optional[Path] = None) -> str:
    root = (root or Path.cwd()).resolve()
    agents = discover_agents()
    skills = discover_skills()
    adapters = list_adapters()
    pkg: Dict[str, Any] = {
        "format": "ventura-agent-package/v1",
        "name": "ventura.gold",
        "version": "1.0.0",
        "authentication": "none-for-local-runtime",
        "portability": adapters,
        "agents": [
            {k: a.get(k) for k in ("id", "name", "description", "capabilities", "version", "author")}
            for a in agents
        ],
        "skills": [
            {k: s.get(k) for k in ("id", "name", "description", "capabilities", "version", "author")}
            for s in skills
        ],
        "adapters": adapters,
    }
    out_dir = root / "dist"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "ventura-agent-package.json"
    out_path.write_text(json.dumps(pkg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return str(out_path)
