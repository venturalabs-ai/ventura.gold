"""
Runtime - Local plan builder for venture.gold.

Builds an execution plan and instruction package without calling external models.
"""

from __future__ import annotations

from typing import Any

from .router import route


def run(prompt: str, agents: list | None = None, skills: list | None = None) -> dict[str, Any]:
    """Build a local plan and instructions from a user prompt."""
    if not prompt or not str(prompt).strip():
        raise ValueError("Prompt vazio")
    if len(prompt) > 100_000:
        raise ValueError("Prompt excedeu 100.000 caracteres")

    routing = route(prompt, agents or [], skills or [])
    agent = routing.get("agent")
    selected_skills = routing.get("skills") or []

    parts: list[str] = []
    if agent:
        parts.append(f"# Agente: {agent.get('name', agent.get('id', 'unknown'))}")
        parts.append(agent.get("instructions") or agent.get("description") or "")
    for skill in selected_skills:
        parts.append(f"# Skill: {skill.get('name', skill.get('id', 'unknown'))}")
        parts.append(skill.get("instructions") or skill.get("description") or "")
    parts.append("---\n# Solicitação do usuário\n\n" + prompt.strip())

    instructions = "\n\n".join(p for p in parts if p)

    return {
        "plan": {
            "prompt": prompt,
            "selectedAgent": agent,
            "selectedSkills": selected_skills,
            "routingReason": routing.get("reason"),
            "scores": routing.get("scores", []),
        },
        "instructions": instructions,
        "adapter": (agent or {}).get("id", "generic"),
        "providerResponse": None,
    }
