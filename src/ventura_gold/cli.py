"""ventura.gold — CLI: framework + agente de repositório."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

import typer

from ventura_gold.core.exporter import export_package
from ventura_gold.core.llm_client import LLMClient
from ventura_gold.core.registry import discover_agents, discover_skills, list_adapters
from ventura_gold.core.runtime import run_prompt
from ventura_gold.core.validator import validate_all
from ventura_gold.skills.code_generator import CodeGeneratorSkill
from ventura_gold.skills.repository_analyst import RepositoryAnalystSkill
from ventura_gold.skills.test_builder import TestBuilderSkill

app = typer.Typer(help="ventura.gold — Agente de Repositório Automatizado (local-first)", no_args_is_help=True)
repo_app = typer.Typer(help="Análise e automação de repositório")
app.add_typer(repo_app, name="repo")


def get_llm(provider: str = "generic") -> LLMClient:
    return LLMClient(provider=provider)


@app.command()
def run(
    prompt: str = typer.Option(..., "--prompt", "-p", help="Solicitação para o agente"),
    provider: str = typer.Option("generic", "--llm", help="Provedor: generic, claude, chatgpt, grok, ..."),
):
    """Executa agente com a solicitação fornecida."""
    result = run_prompt(prompt, Path.cwd(), provider)
    typer.echo(f"\n✅ Agente selecionado: {result.get('agent') or 'Nenhum'}")
    typer.echo(f"🧠 Motivo: {result.get('reason', '')}")
    typer.echo("\n" + "=" * 60)
    typer.echo(result.get("instructions", ""))
    typer.echo("=" * 60)
    if result.get("mode") == "local":
        typer.echo("\nℹ️  [MODO LOCAL] — sem chamada de API. Instruções prontas para copiar.")
    else:
        typer.echo(f"\n🤖 Resposta de {provider}:")
        typer.echo(result.get("response") or "(vazio)")


@app.command("list")
def list_cmd():
    """Lista agentes, skills e adaptadores."""
    agents = discover_agents(Path.cwd())
    skills = discover_skills(Path.cwd())
    adapters = list_adapters()
    typer.echo(f"\n🤖 Agentes ({len(agents)}):")
    for a in agents:
        typer.echo(f"  • {a.get('id')}: {a.get('name')}")
    typer.echo(f"\n📚 Skills ({len(skills)}):")
    for s in skills:
        typer.echo(f"  • {s.get('id')}: {s.get('name')}")
    typer.echo(f"\n🔌 Adaptadores ({len(adapters)}):")
    for name in adapters:
        typer.echo(f"  • {name}")


@app.command()
def validate():
    """Valida integridade do projeto."""
    errors, warnings = validate_all(Path.cwd())
    if errors:
        typer.echo("\n❌ ERROS:", err=True)
        for e in errors:
            typer.echo(f"  ✗ {e}", err=True)
        raise typer.Exit(1)
    if warnings:
        typer.echo("\n⚠️ Avisos:")
        for wmsg in warnings:
            typer.echo(f"  • {wmsg}")
    typer.echo("\n✅ Validação aprovada")


@app.command()
def doctor():
    """Diagnóstico do ambiente."""
    import os

    api_keys = [k for k in os.environ if k.endswith("_API_KEY")]
    agents = discover_agents(Path.cwd())
    skills = discover_skills(Path.cwd())
    adapters = list_adapters()
    typer.echo("🏥 Diagnóstico do ambiente:\n")
    typer.echo(f"✅ Python: {sys.version.split()[0]}")
    typer.echo("✅ Modo local: SEM AUTENTICAÇÃO OBRIGATÓRIA")
    typer.echo(f"✅ Agentes: {len(agents)} | Skills: {len(skills)} | Adaptadores: {len(adapters)}")
    if api_keys:
        typer.echo(f"ℹ️  Chaves de API configuradas: {', '.join(api_keys)}")
    else:
        typer.echo("ℹ️  Nenhuma chave de API — modo local funcionando")
    typer.echo("\n✅ Sistema pronto.")


@app.command()
def export():
    """Gera pacote portátil JSON."""
    path = export_package(Path.cwd())
    typer.echo(f"✅ Pacote gerado: {path}")


@repo_app.command("scan")
def repo_scan():
    """Analisa e gera relatório completo do repositório."""
    skill = RepositoryAnalystSkill(Path.cwd())
    typer.echo(skill.generate_report())


@repo_app.command("generate-code")
def generate_code(
    spec: str = typer.Option(..., "--spec", "-s", help="Especificação do código"),
    provider: str = typer.Option("generic", "--llm", help="Provedor de IA"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Salvar em arquivo"),
):
    """Gera código Python a partir de especificação (API opcional)."""
    skill = CodeGeneratorSkill(get_llm(provider))
    result = skill.create_module(spec)
    if not result["success"]:
        typer.echo(f"⚠️ Modo local / falha API: {result.get('error')}")
    if result.get("explanation"):
        typer.echo(result["explanation"])
    typer.echo("\n📝 Código Gerado:")
    typer.echo(f"```python\n{result['content']}\n```")
    if output:
        output.write_text(result["content"], encoding="utf-8")
        typer.echo(f"\n✅ Salvo em: {output}")


@repo_app.command("generate-tests")
def generate_tests(
    file: Path = typer.Option(..., "--file", "-f", help="Arquivo .py para testar"),
    provider: str = typer.Option("generic", "--llm", help="Provedor de IA"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Arquivo de teste"),
):
    """Gera testes automaticamente para um arquivo Python (API opcional)."""
    skill = TestBuilderSkill(get_llm(provider))
    code = file.read_text(encoding="utf-8")
    result = skill.generate_tests(code, module_name=file.stem)
    if not result.get("test_code"):
        typer.echo("⚠️ Modo local — sem chave de IA ou sem bloco de código. Teste não gerado via LLM.")
        typer.echo(result.get("explanation") or result.get("error") or "")
        return
    if result.get("explanation"):
        typer.echo(result["explanation"])
    typer.echo(f"\n🧪 Testes:\n```python\n{result['test_code']}\n```")
    if output:
        output.write_text(result["test_code"], encoding="utf-8")
        typer.echo(f"✅ Salvo em: {output}")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
