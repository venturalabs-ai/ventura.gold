"""Local runtime — builds plans; optional LLM call via client."""
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

    agents = discover_agents()
    skills = discover_skills()
    routing = route(prompt, agents, skills)
    agent = routing.get("agent")
    selected_skills = routing.get("skills") or []

    parts: list[str] = []
    if agent:
        parts.append(f"# Agente: {agent.get('name', agent.get('id'))}")
        parts.append(agent.get("instructions") or agent.get("description") or "")
    for skill in selected_skills:
        parts.append(f"# Skill: {skill.get('name', skill.get('id'))}")
        parts.append(skill.get("instructions") or skill.get("description") or "")
    parts.append("---\n# Solicitação do usuário\n\n" + prompt.strip())
    instructions = "\n\n".join(p for p in parts if p)

    client = LLMClient(provider=provider)
    llm = client.generate_sync(prompt, system_prompt=instructions)

    return {
        "agent": (agent or {}).get("name"),
        "agent_id": (agent or {}).get("id"),
        "skills": [s.get("name") for s in selected_skills],
        "reason": routing.get("reason"),
        "instructions": instructions,
        "response": llm.text if llm.mode == "api" and llm.success else None,
        "mode": llm.mode,
        "provider": provider,
        "providerResponse": llm.text if llm.mode == "api" and llm.success else None,
    }
