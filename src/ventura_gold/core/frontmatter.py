"""Lightweight frontmatter parser for agent/skill Markdown files."""
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Tuple


def parse_frontmatter(content: str) -> Tuple[Dict[str, Any], str]:
    """Return (metadata, body). If no frontmatter, metadata is {}."""
    match = re.match(r"^---\s*\n([\s\S]*?)\n---\s*\n?(.*)$", content, re.DOTALL)
    if not match:
        return {}, content.strip()

    meta: Dict[str, Any] = {}
    for line in match.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            meta[key] = [v.strip().strip('"').strip("'") for v in inner.split(",") if v.strip()] if inner else []
        elif value.lower() == "true":
            meta[key] = True
        elif value.lower() == "false":
            meta[key] = False
        else:
            meta[key] = value
    return meta, match.group(2).strip()


def is_valid_meta(meta: Dict[str, Any], required: Optional[List[str]] = None) -> bool:
    required = required or ["id", "name", "description", "capabilities", "version", "author"]
    for field in required:
        if field not in meta or meta[field] in (None, "", []):
            return False
    return True
