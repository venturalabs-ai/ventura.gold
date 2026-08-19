"""
Router - Deterministic capability-based routing.

Normalizes text (accents and case), matches prompt against agent/skill names,
descriptions and capabilities, scores matches, and provides predictable
fallback when no correspondence is found.
"""

from __future__ import annotations

import re
import unicodedata
from typing import Any


def normalize_text(text: str) -> str:
    """Normalize text: lower case, remove accents, remove special chars."""
    text = unicodedata.normalize("NFD", text or "")
    text = re.sub(r"[\u0300-\u036f]", "", text)
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def score_candidate(candidate: dict[str, Any], prompt: str) -> int:
    """Score how well a candidate matches a prompt."""
    normalized_prompt = normalize_text(prompt)
    normalized_name = normalize_text(candidate.get("name", ""))
    normalized_desc = normalize_text(candidate.get("description", ""))
    normalized_caps = [normalize_text(str(c)) for c in candidate.get("capabilities", [])]

    score = 0
    prompt_words = [w for w in normalized_prompt.split() if len(w) > 2]

    if normalized_prompt and normalized_prompt == normalized_name:
        score += 100
    elif normalized_prompt and normalized_prompt in normalized_name:
        score += 70
    else:
        name_words = [w for w in normalized_name.split() if len(w) > 2]
        score += sum(15 for w in prompt_words if w in name_words)

    if normalized_prompt and normalized_prompt in normalized_desc:
        score += 50
    else:
        desc_words = [w for w in normalized_desc.split() if len(w) > 2]
        score += sum(10 for w in prompt_words if w in desc_words)

    for cap in normalized_caps:
        if normalized_prompt and normalized_prompt in cap:
            score += 30
        else:
            cap_words = [w for w in cap.split() if len(w) > 2]
            score += sum(5 for w in prompt_words if w in cap_words)

    return score


def route(prompt: str, agents: list | None = None, skills: list | None = None) -> dict[str, Any]:
    """Route a prompt to the best matching agent and skills."""
    agents = agents or []
    skills = skills or []

    scored_agents = sorted(
        ({"item": a, "score": score_candidate(a, prompt)} for a in agents),
        key=lambda x: (-x["score"], x["item"].get("id", "")),
    )
    scored_skills = sorted(
        ({"item": s, "score": score_candidate(s, prompt)} for s in skills),
        key=lambda x: (-x["score"], x["item"].get("id", "")),
    )

    best_agent = scored_agents[0] if scored_agents else None
    selected_skills = [s["item"] for s in scored_skills if s["score"] >= 12]

    if best_agent and best_agent["score"] > 0:
        reason = f"Melhor correspondência com pontuação {best_agent['score']}"
        agent = best_agent["item"]
    elif scored_agents:
        orch = next((s for s in scored_agents if s["item"].get("id") == "orchestrator"), scored_agents[0])
        agent = orch["item"]
        reason = "Nenhuma correspondência forte — usando agente padrão"
    else:
        agent = None
        reason = "Nenhum agente registrado"

    return {
        "agent": agent,
        "skills": selected_skills,
        "scores": [{"id": s["item"].get("id"), "score": s["score"]} for s in scored_agents],
        "reason": reason,
    }
