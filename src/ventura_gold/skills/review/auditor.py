"""Skill: code review and audit — offline heuristics + optional LLM."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from ventura_gold.core.llm_client import LLMClient
from ventura_gold.mcp.server_filesystem import FileSystemServer
from ventura_gold.mcp.server_git import GitServer


class ReviewAuditorSkill:
    SECRET_PATTERNS = [
        re.compile(r"sk-[a-zA-Z0-9]{20,}"),
        re.compile(r"(?i)(api[_-]?key|secret|password)\s*=\s*['\"][^'\"]{8,}['\"]"),
    ]

    def __init__(self, llm: Optional[LLMClient] = None, repo_path: Optional[Path] = None):
        self.llm = llm or LLMClient(provider="generic")
        self.repo_path = (repo_path or Path.cwd()).resolve()
        self.git = GitServer(self.repo_path)
        self.fs = FileSystemServer(self.repo_path)

    def audit(self) -> Dict[str, Any]:
        files = self.git.ls() or [
            str(p.relative_to(self.repo_path))
            for p in self.repo_path.rglob("*.py")
            if p.is_file() and ".git" not in p.parts and "__pycache__" not in p.parts
        ][:100]
        findings: List[Dict[str, str]] = []
        py_files = [f for f in files if f.endswith(".py")]
        for f in py_files[:40]:
            analysis = self.fs.analyze_python(f)
            if not analysis.get("valid_syntax"):
                findings.append({"file": f, "level": "error", "message": str(analysis.get("error", "syntax"))})
            content = self.fs.read(f) or ""
            for pat in self.SECRET_PATTERNS:
                if pat.search(content):
                    findings.append({"file": f, "level": "critical", "message": "Possivel segredo hardcoded"})
                    break
        return {
            "python_files_scanned": len(py_files[:40]),
            "findings": findings,
            "ok": not any(x["level"] == "critical" for x in findings),
        }

    def report(self) -> str:
        data = self.audit()
        lines = [
            "# Relatorio de Revisao / Auditoria",
            "",
            f"Arquivos Python analisados: **{data['python_files_scanned']}**",
            f"Status: **{'OK' if data['ok'] else 'ATENCAO'}**",
            "",
        ]
        if not data["findings"]:
            lines.append("Nenhum achado critico nas heuristicas locais.")
        else:
            lines.append("## Achados")
            for f in data["findings"]:
                lines.append(f"- [{f['level']}] `{f['file']}`: {f['message']}")
        lines.append("")
        lines.append("> Gerado por ventura.gold skills/review (modo local)")
        return "\n".join(lines)
