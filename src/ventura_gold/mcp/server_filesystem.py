"""Servidor MCP-style — filesystem com proteção de path traversal."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Dict, List, Optional


class FileSystemServer:
    def __init__(self, root: Optional[Path] = None):
        self.root = (root or Path.cwd()).resolve()

    def _safe_path(self, rel_path: str) -> Path:
        full = (self.root / rel_path).resolve()
        if not str(full).startswith(str(self.root)):
            raise PermissionError(f"Caminho fora do repositório: {rel_path}")
        return full

    def list_dir(self, rel_path: str = ".", pattern: str = "*") -> List[str]:
        path = self._safe_path(rel_path)
        if not path.exists():
            return []
        return sorted(f.name for f in path.glob(pattern) if f.is_file())

    def read(self, rel_path: str) -> Optional[str]:
        path = self._safe_path(rel_path)
        return path.read_text(encoding="utf-8") if path.exists() else None

    def write(self, rel_path: str, content: str) -> bool:
        path = self._safe_path(rel_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return True

    def analyze_python(self, rel_path: str) -> Dict:
        code = self.read(rel_path)
        if not code:
            return {"error": "Arquivo não encontrado", "valid_syntax": False}
        try:
            tree = ast.parse(code)
            return {
                "file": rel_path,
                "classes": [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)],
                "functions": [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)],
                "imports": len(
                    [n for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))]
                ),
                "lines": len(code.splitlines()),
                "valid_syntax": True,
            }
        except SyntaxError as e:
            return {"file": rel_path, "valid_syntax": False, "error": str(e), "line": e.lineno}
