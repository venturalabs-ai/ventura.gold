"""Runtime local — monta plano/instruções; LLM opcional via LLMClient."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

from .llm_client import LLMClient
from .registry import discover_agents, discover_skills
from .router import route


def run_prompt(
    prompt: str,
    root: Optional[Path] = None,
    provider: str = "generic",
) -> Dict[str, Any]:
    if not prompt or not str(prompt).strip():
        raise ValueError("Prompt vazio")
    if len(prompt) > 100_000:
        raise ValueError("Prompt excedeu 100.000 caracteres")

    root = root or Path.cwd()
    agents = discover_agents(root)
    skills = discover_skills(root)
    routing = route(prompt, agents, skills)
    agent = routing.get("agent")
    selected = routing.get("skills") or []

    parts = []
    if agent:
        parts.append(f"# Agente: {agent.get('name')}")
        parts.append(agent.get("instructions") or agent.get("description") or "")
    for skill in selected:
        parts.append(f"# Skill: {skill.get('name')}")
        parts.append(skill.get("instructions") or skill.get("description") or "")
    parts.append("---\n# Solicitação do usuário\n\n" + prompt.strip())
    instructions = "\n\n".join(p for p in parts if p)

    client = LLMClient(provider=provider)
    response_text = ""
    if client.mode == "api":
        llm_resp = client.generate(prompt, system_prompt=instructions)
        response_text = llm_resp.text if llm_resp.success else ""

    return {
        "agent": (agent or {}).get("name"),
        "agent_id": (agent or {}).get("id"),
        "skills": [s.get("name") for s in selected],
        "reason": routing.get("reason"),
        "instructions": instructions,
        "mode": client.mode,
        "provider": provider,
        "response": response_text,
        "providerResponse": response_text if response_text else None,
    }
