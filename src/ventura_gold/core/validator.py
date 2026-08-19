"""Validação de integridade e segurança básica."""

from __future__ import annotations

import re
from pathlib import Path
from typing import List, Optional, Tuple

_SECRET_RE = re.compile(
    r"(?<![A-Za-z0-9_])(sk-ant-[A-Za-z0-9_-]{10,}|sk-proj-[A-Za-z0-9_-]{10,}|ghp_[A-Za-z0-9]{20,}|xai-[A-Za-z0-9]{20,})"
)


def validate_all(root: Optional[Path] = None) -> Tuple[List[str], List[str]]:
    root = root or Path.cwd()
    errors: List[str] = []
    warnings: List[str] = []

    required = [
        "src/ventura_gold/core/router.py",
        "src/ventura_gold/core/runtime.py",
        "src/ventura_gold/cli.py",
        "pyproject.toml",
    ]
    for rel in required:
        if not (root / rel).exists():
            warnings.append(f"Path not found in cwd (ok if installed package only): {rel}")

    src = root / "src"
    if src.exists():
        for path in src.rglob("*.py"):
            if path.name in {"validator.py"}:
                continue
            try:
                content = path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            if _SECRET_RE.search(content):
                errors.append(f"Possible secret pattern in {path.relative_to(root)}")

    return errors, warnings
