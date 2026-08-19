#!/usr/bin/env python3
"""ventura.gold — local-first repository agent CLI."""
from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path
from typing import Optional

import typer

from ventura_gold.core.exporter import export_package
from ventura_gold.core.llm_client import LLMClient
from ventura_gold.core.registry import discover_agents, discover_skills, list_adapters
from ventura_gold.core.runtime import run_prompt
from ventura_gold.core.validator import validate_all
from ventura_gold.skills.codegen.generator import CodeGeneratorSkill
from ventura_gold.skills.repository.analyst import RepositoryAnalystSkill
from ventura_gold.skills.testing.builder import TestBuilderSkill
from ventura_gold.skills.docs.generator import DocsGeneratorSkill
from ventura_gold.skills.review.auditor import ReviewAuditorSkill

app = typer.Typer(help="ventura.gold — Agente de Repositorio (local-first)", no_args_is_help=True)
repo_app = typer.Typer(help="Analise e automacao de repositorio")
app.add_typer(repo_app, name="repo")


def get_llm(provider: str = "generic") -> LLMClient:
    return LLMClient(provider=provider)


@app.command("run")
def run_cmd(
    prompt: str = typer.Option(..., "--prompt", "-p", help="Solicitacao para o agente"),
    provider: str = typer.Option("generic", "--llm", help="Provedor: generic, claude, chatgpt, ..."),
):
    """Executa agente (plano local; API opcional)."""
    result = run_prompt(prompt, Path.cwd(), provider)
    typer.echo(f"\nOK Agente selecionado: {result.get('agent') or 'Nenhum'}")
    typer.echo(f"Motivo: {result.get('reason', '')}")
    typer.echo("\n" + "=" * 60)
    typer.echo(result.get("instructions", ""))
    typer.echo("=" * 60)
    if result.get("mode") == "local":
        typer.echo("\n[MODO LOCAL] — sem chamada de API. Instrucoes prontas para usar.")
    elif result.get("response"):
        typer.echo(f"\nResposta de {provider}:")
        typer.echo(result["response"])


@app.command("list")
def list_cmd():
    """Lista agentes, skills e adaptadores."""
    agents = discover_agents()
    skills = discover_skills()
    adapters = list_adapters()
    typer.echo(f"\nAgentes ({len(agents)}):")
    for a in agents:
        typer.echo(f"  - {a.get('id')}: {a.get('name')}")
    typer.echo(f"\nSkills ({len(skills)}):")
    for s in skills:
        typer.echo(f"  - {s.get('id')}: {s.get('name')}")
    typer.echo(f"\nAdaptadores ({len(adapters)}):")
    for a in adapters:
        typer.echo(f"  - {a}")


@app.command("validate")
def validate_cmd():
    """Valida integridade do projeto."""
    errors, warnings = validate_all(Path.cwd())
    if errors:
        typer.echo("\nERROS:", err=True)
        for e in errors:
            typer.echo(f"  x {e}", err=True)
        raise typer.Exit(1)
    if warnings:
        typer.echo("\nAvisos:")
        for wmsg in warnings:
            typer.echo(f"  - {wmsg}")
    typer.echo("\nValidacao aprovada")


@app.command("doctor")
def doctor_cmd():
    """Diagnostico do ambiente."""
    agents = discover_agents()
    skills = discover_skills()
    adapters = list_adapters()
    api_keys = [k for k in os.environ if k.endswith("_API_KEY")]
    typer.echo("Diagnostico do ambiente:\n")
    typer.echo(f"Python: {sys.version.split()[0]}")
    typer.echo("Modo local: SEM AUTENTICACAO OBRIGATORIA")
    typer.echo(f"Agentes: {len(agents)} | Skills: {len(skills)} | Adaptadores: {len(adapters)}")
    if api_keys:
        typer.echo(f"Chaves de API configuradas: {', '.join(api_keys)}")
    else:
        typer.echo("Nenhuma chave de API — modo local funcionando")
    typer.echo("\nSistema pronto.")


@app.command("export")
def export_cmd():
    """Gera pacote portatil JSON."""
    path = export_package(Path.cwd())
    typer.echo(f"Pacote gerado: {path}")


@repo_app.command("scan")
def repo_scan():
    """Analisa e gera relatorio do repositorio (offline)."""
    skill = RepositoryAnalystSkill(Path.cwd())
    typer.echo(skill.generate_report())


@repo_app.command("generate-code")
def generate_code(
    spec: str = typer.Option(..., "--spec", "-s", help="Especificacao do codigo"),
    provider: str = typer.Option("generic", "--llm", help="Provedor de IA"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Salvar em arquivo"),
):
    """Gera codigo Python a partir de especificacao."""
    skill = CodeGeneratorSkill(get_llm(provider))
    result = asyncio.run(skill.create_module(spec))
    typer.echo(result.get("explanation") or "")
    typer.echo("\nCodigo:")
    typer.echo(result.get("content") or "")
    if result.get("mode") == "local":
        typer.echo("\nModo local — cole o prompt em uma IA ou configure *_API_KEY.")
    if output and result.get("content"):
        output.write_text(result["content"], encoding="utf-8")
        typer.echo(f"\nSalvo em: {output}")


@repo_app.command("generate-tests")
def generate_tests(
    file: Path = typer.Option(..., "--file", "-f", help="Arquivo .py para testar"),
    provider: str = typer.Option("generic", "--llm", help="Provedor de IA"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Arquivo de teste"),
):
    """Gera testes (API opcional; modo local devolve template)."""
    if not file.exists():
        typer.echo(f"Arquivo nao encontrado: {file}", err=True)
        raise typer.Exit(1)
    skill = TestBuilderSkill(get_llm(provider))
    code = file.read_text(encoding="utf-8")
    result = asyncio.run(skill.generate_tests(code, module_name=file.stem))
    if result.get("mode") == "local" and not result.get("test_code"):
        template = (
            f'"""Tests for {file.stem} — gerado em modo local."""\n'
            "import pytest\n\n"
            f"# TODO: implement tests for {file.stem}\n"
            f"# Fonte: {file}\n\n"
            "def test_placeholder():\n"
            "    assert True\n"
        )
        result["test_code"] = template
        result["explanation"] = "Template local (sem chave de API)."
    typer.echo(result.get("explanation") or "")
    typer.echo("\nTestes:\n")
    typer.echo(result.get("test_code") or "")
    if output and result.get("test_code"):
        output.write_text(result["test_code"], encoding="utf-8")
        typer.echo(f"Salvo em: {output}")


@repo_app.command("docs")
def repo_docs():
    """Gera outline de documentacao do repositorio (offline)."""
    skill = DocsGeneratorSkill(repo_path=Path.cwd())
    typer.echo(skill.generate_readme_outline())


@repo_app.command("review")
def repo_review():
    """Revisao/auditoria heuristica local do codigo."""
    skill = ReviewAuditorSkill(repo_path=Path.cwd())
    typer.echo(skill.report())


def main() -> None:
    app()


if __name__ == "__main__":
    main()
