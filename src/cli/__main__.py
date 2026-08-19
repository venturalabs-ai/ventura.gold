#!/usr/bin/env python3
"""CLI for ventura.gold — local-first agent framework."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from core.registry import discover_agents, discover_skills  # noqa: E402
from core.runtime import run  # noqa: E402
from core.exporter import export_package  # noqa: E402
from core.validator import validate_project  # noqa: E402


def list_adapters() -> list[str]:
    adapters_dir = ROOT / "src" / "adapters"
    if not adapters_dir.exists():
        return []
    return sorted(p.stem for p in adapters_dir.glob("*.py") if p.name != "__init__.py")


def cmd_run(prompt: str) -> int:
    agents = discover_agents()
    skills = discover_skills()
    result = run(prompt, agents, skills)
    plan = result["plan"]
    agent = plan.get("selectedAgent") or {}
    skills_sel = plan.get("selectedSkills") or []
    print("✅ Execução concluída (modo local — sem chamada a modelo externo)")
    print("📋 Agente selecionado:", agent.get("name") or "Nenhum")
    print("📚 Skills selecionadas:", ", ".join(s.get("name", s.get("id", "?")) for s in skills_sel) or "Nenhuma")
    print("🧠 Motivo:", plan.get("routingReason"))
    print("\n" + "=" * 60)
    print("INSTRUÇÕES MONTADAS:\n")
    print(result["instructions"])
    print("\n" + "=" * 60)
    print("ℹ️  providerResponse: null (modo simulado local)")
    return 0


def cmd_list() -> int:
    agents = discover_agents()
    skills = discover_skills()
    adapters = list_adapters()
    print(f"\n🤖 Agentes ({len(agents)}):")
    for a in agents:
        print(f"  • {a.get('id')}: {a.get('name')}")
    print(f"\n📚 Skills ({len(skills)}):")
    for s in skills:
        print(f"  • {s.get('id')}: {s.get('name')}")
    print(f"\n🔌 Adaptadores ({len(adapters)}):")
    for a in adapters:
        print(f"  • {a}")
    return 0


def cmd_doctor() -> int:
    agents = discover_agents()
    skills = discover_skills()
    adapters = list_adapters()
    print("🏥 Diagnóstico do ambiente:\n")
    print(f"✅ Python: {sys.version.split()[0]}")
    print("✅ Modo local: SEM AUTENTICAÇÃO OBRIGATÓRIA")
    print(f"✅ Agentes: {len(agents)} | Skills: {len(skills)} | Adaptadores: {len(adapters)}")
    print("\n✅ Sistema pronto para uso local.")
    return 0


def cmd_validate() -> int:
    result = validate_project(ROOT)
    agents = discover_agents()
    skills = discover_skills()
    if not agents:
        result["errors"].append({"file": "src/agents", "message": "Nenhum agente válido encontrado"})
        result["valid"] = False
    if not skills:
        result["errors"].append({"file": "src/skills", "message": "Nenhuma skill válida encontrada"})
        result["valid"] = False
    if result["errors"]:
        print("\n❌ ERROS:")
        for e in result["errors"]:
            print(f"  ✗ {e.get('file')}: {e.get('message')}")
    if result["valid"]:
        print("\n✅ Validação aprovada")
        return 0
    return 1


def cmd_export() -> int:
    agents = discover_agents()
    skills = discover_skills()
    adapters = list_adapters()
    out = export_package(agents, skills, adapters, ROOT)
    print(f"✅ Pacote gerado: {out['path']}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ventura-gold", description="ventura.gold local-first agent CLI")
    sub = parser.add_subparsers(dest="command")

    p_run = sub.add_parser("run", help="Montar plano e instruções")
    p_run.add_argument("--prompt", required=True, help="Solicitação do usuário")

    sub.add_parser("list", help="Listar agentes, skills e adaptadores")
    sub.add_parser("doctor", help="Diagnóstico do ambiente")
    sub.add_parser("validate", help="Validar projeto")
    sub.add_parser("export", help="Exportar pacote portátil")

    parser.add_argument("--prompt", help="Atalho para run --prompt")

    args = parser.parse_args(argv)

    if args.prompt and not args.command:
        return cmd_run(args.prompt)
    if args.command == "run":
        return cmd_run(args.prompt)
    if args.command == "list":
        return cmd_list()
    if args.command == "doctor":
        return cmd_doctor()
    if args.command == "validate":
        return cmd_validate()
    if args.command == "export":
        return cmd_export()

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
