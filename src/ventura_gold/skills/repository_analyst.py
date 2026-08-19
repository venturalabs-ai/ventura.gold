"""Skill: Analista de Repositório."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional

from ventura_gold.mcp.server_filesystem import FileSystemServer
from ventura_gold.mcp.server_git import GitServer


class RepositoryAnalystSkill:
    def __init__(self, repo_path: Optional[Path] = None):
        self.repo_path = (repo_path or Path.cwd()).resolve()
        self.git = GitServer(self.repo_path)
        self.fs = FileSystemServer(self.repo_path)

    def scan(self) -> Dict:
        status = self.git.status()
        files = self.git.ls()
        if not files and status.get("branch") in ("n/a", "error", ""):
            files = [
                str(p.relative_to(self.repo_path))
                for p in self.repo_path.rglob("*")
                if p.is_file() and ".git" not in p.parts and "node_modules" not in p.parts
            ][:500]

        py_files = [f for f in files if f.endswith(".py")]
        md_files = [f for f in files if f.endswith(".md")]
        analysis = {
            "status": status,
            "stats": {
                "total_files": len(files),
                "python_files": len(py_files),
                "markdown_files": len(md_files),
            },
            "python_analysis": [self.fs.analyze_python(f) for f in py_files[:30]],
            "readme_exists": any(f.upper() == "README.MD" or f == "README.md" for f in files),
            "license_exists": any("LICENSE" in f.upper() for f in files),
            "tests_exist": any("test" in f.lower() for f in files),
            "files_sample": files[:40],
        }
        return analysis

    def generate_report(self) -> str:
        data = self.scan()
        valid = sum(1 for a in data["python_analysis"] if a.get("valid_syntax"))
        total = len(data["python_analysis"])
        quality = f"- Sintaxe válida: {valid}/{total}" if total else "- Sem arquivos Python analisados"
        return f"""# Relatório do Repositório

## Estado Geral
- **Branch:** `{data['status'].get('branch')}`
- **Commit:** `{data['status'].get('commit')}`
- **Arquivos modificados:** {len(data['status'].get('modified') or [])}
- **Arquivos não rastreados:** {len(data['status'].get('untracked') or [])}

## Estatísticas
- Total de arquivos: {data['stats']['total_files']}
- Arquivos Python: {data['stats']['python_files']}
- Documentação: {data['stats']['markdown_files']}
- README: {'✅' if data['readme_exists'] else '❌'}
- Licença: {'✅' if data['license_exists'] else '❌'}
- Testes: {'✅' if data['tests_exist'] else '❌'}

## Qualidade do Código
{quality}

> Relatório gerado automaticamente por ventura.gold
"""
