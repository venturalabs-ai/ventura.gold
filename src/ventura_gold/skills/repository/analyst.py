"""Skill: repository analyst — offline scan and markdown report."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from ventura_gold.mcp.server_filesystem import FileSystemServer
from ventura_gold.mcp.server_git import GitServer


class RepositoryAnalystSkill:
    def __init__(self, repo_path: Optional[Path] = None):
        self.repo_path = (repo_path or Path.cwd()).resolve()
        self.git = GitServer(self.repo_path)
        self.fs = FileSystemServer(self.repo_path)

    def scan(self) -> Dict[str, Any]:
        status = self.git.status()
        files = self.git.ls()
        if not files:
            files = [
                str(p.relative_to(self.repo_path))
                for p in self.repo_path.rglob("*")
                if p.is_file() and ".git" not in p.parts and "__pycache__" not in p.parts
            ][:500]
        py_files = [f for f in files if f.endswith(".py")]
        md_files = [f for f in files if f.endswith(".md")]
        analyses: List[Dict[str, Any]] = []
        for f in py_files[:30]:
            try:
                analyses.append(self.fs.analyze_python(f))
            except Exception as e:
                analyses.append({"file": f, "valid_syntax": False, "error": str(e)})
        return {
            "status": status,
            "stats": {
                "total_files": len(files),
                "python_files": len(py_files),
                "markdown_files": len(md_files),
            },
            "python_analysis": analyses,
            "readme_exists": any(f.endswith("README.md") for f in files),
            "license_exists": any("LICENSE" in f.upper() for f in files),
            "tests_exist": any("test" in f.lower() for f in files),
        }

    def generate_report(self) -> str:
        data = self.scan()
        valid = sum(1 for a in data["python_analysis"] if a.get("valid_syntax"))
        total = len(data["python_analysis"])
        quality = f"- Sintaxe valida: {valid}/{total}" if total else "- Sem arquivos Python analisados"
        return (
            "# Relatorio do Repositorio\n\n"
            f"## Estado Geral\n"
            f"- **Branch:** `{data['status'].get('branch')}`\n"
            f"- **Commit:** `{data['status'].get('commit')}`\n"
            f"- **Arquivos modificados:** {len(data['status'].get('modified') or [])}\n"
            f"- **Arquivos nao rastreados:** {len(data['status'].get('untracked') or [])}\n\n"
            f"## Estatisticas\n"
            f"- Total de arquivos: {data['stats']['total_files']}\n"
            f"- Arquivos Python: {data['stats']['python_files']}\n"
            f"- Documentacao: {data['stats']['markdown_files']}\n"
            f"- README: {'sim' if data['readme_exists'] else 'nao'}\n"
            f"- Licenca: {'sim' if data['license_exists'] else 'nao'}\n"
            f"- Testes: {'sim' if data['tests_exist'] else 'nao'}\n\n"
            f"## Qualidade do Codigo\n{quality}\n\n"
            "> Relatorio gerado automaticamente por ventura.gold (modo local)\n"
        )
