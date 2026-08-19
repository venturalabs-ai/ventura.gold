"""Servidor MCP-style — operações Git seguras (somente leitura por padrão)."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Dict, List, Optional


class GitServer:
    def __init__(self, repo_path: Optional[Path] = None):
        self.repo_path = (repo_path or Path.cwd()).resolve()

    def run_git(self, *args: str) -> str:
        try:
            r = subprocess.run(
                ["git", *args],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=30,
            )
            return (r.stdout or "").strip()
        except Exception as e:
            return f"error: {e}"

    def status(self) -> Dict:
        return {
            "branch": self.run_git("rev-parse", "--abbrev-ref", "HEAD") or "n/a",
            "commit": self.run_git("rev-parse", "--short", "HEAD") or "n/a",
            "modified": [x for x in self.run_git("diff", "--name-only").splitlines() if x],
            "untracked": [
                x
                for x in self.run_git("ls-files", "--others", "--exclude-standard").splitlines()
                if x
            ],
        }

    def log(self, limit: int = 10) -> List[Dict]:
        lines = self.run_git(
            "log", f"-n{limit}", "--format=%h|%s|%an|%ad", "--date=short"
        ).splitlines()
        out = []
        for line in lines:
            if not line or "|" not in line:
                continue
            parts = line.split("|", 3)
            if len(parts) == 4:
                out.append(dict(zip(["hash", "message", "author", "date"], parts)))
        return out

    def ls(self) -> List[str]:
        return [x for x in self.run_git("ls-files").splitlines() if x]

    def read_file(self, path: str) -> Optional[str]:
        full = (self.repo_path / path).resolve()
        if not str(full).startswith(str(self.repo_path)):
            return None
        if full.exists() and full.is_file():
            return full.read_text(encoding="utf-8", errors="replace")
        return None
