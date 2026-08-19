"""Skill: documentation generator — local-first Markdown docs."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

from ventura_gold.core.llm_client import LLMClient
from ventura_gold.mcp.server_filesystem import FileSystemServer
from ventura_gold.mcp.server_git import GitServer


class DocsGeneratorSkill:
    def __init__(self, llm: Optional[LLMClient] = None, repo_path: Optional[Path] = None):
        self.llm = llm or LLMClient(provider="generic")
        self.repo_path = (repo_path or Path.cwd()).resolve()
        self.git = GitServer(self.repo_path)
        self.fs = FileSystemServer(self.repo_path)

    def generate_readme_outline(self) -> str:
        files = self.git.ls() or [
            str(p.relative_to(self.repo_path))
            for p in self.repo_path.rglob("*")
            if p.is_file() and ".git" not in p.parts
        ][:200]
        py = sum(1 for f in files if f.endswith(".py"))
        md = sum(1 for f in files if f.endswith(".md"))
        return (
            "# Documentacao do Projeto\n\n"
            f"## Visao geral\n"
            f"Projeto com aproximadamente **{len(files)}** arquivos rastreados ({py} Python, {md} Markdown).\n\n"
            "## Estrutura sugerida\n"
            "- `README.md` — visao e quick start\n"
            "- `docs/INSTALLATION.md` — instalacao\n"
            "- `docs/ARCHITECTURE.md` — arquitetura\n\n"
            "## Proximos passos\n"
            "1. Descrever o problema que o projeto resolve\n"
            "2. Documentar comandos CLI principais\n"
            "3. Listar requisitos e limitacoes (local-first)\n\n"
            "> Gerado por ventura.gold skills/docs (modo local)\n"
        )

    async def generate_module_doc(self, rel_path: str) -> Dict[str, Any]:
        code = self.fs.read(rel_path) or ""
        prompt = f"Documente este modulo Python em Markdown:\n\n```python\n{code[:8000]}\n```"
        resp = await self.llm.generate(prompt, "Voce escreve documentacao tecnica clara em PT-BR.")
        return {"success": resp.success, "content": resp.text, "mode": resp.mode, "error": resp.error}
