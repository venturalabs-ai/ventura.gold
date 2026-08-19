"""Roteamento determinístico por pontuação."""

from __future__ import annotations

import re
import unicodedata
from typing import Any, Dict, List, Optional


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFD", text or "")
    text = re.sub(r"[\u0300-\u036f]", "", text)
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def score_candidate(candidate: dict[str, Any], prompt: str) -> int:
    p = normalize_text(prompt)
    name = normalize_text(candidate.get("name", ""))
    desc = normalize_text(candidate.get("description", ""))
    caps = [normalize_text(str(c)) for c in candidate.get("capabilities", [])]
    score = 0
    words = [w for w in p.split() if len(w) > 2]
    if p and p == name:
        score += 100
    elif p and p in name:
        score += 70
    else:
        score += sum(15 for w in words if w in name.split())
    if p and p in desc:
        score += 50
    else:
        score += sum(10 for w in words if w in desc.split())
    for cap in caps:
        if p and p in cap:
            score += 30
        else:
            score += sum(5 for w in words if w in cap.split())
    return score


def route(
    prompt: str,
    agents: Optional[List[dict[str, Any]]] = None,
    skills: Optional[List[dict[str, Any]]] = None,
) -> Dict[str, Any]:
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
    selected_skills = [s["item"] for s in scored_skills if s["score"] >= 12]
    if scored_agents and scored_agents[0]["score"] > 0:
        agent = scored_agents[0]["item"]
        reason = f"Melhor correspondência com pontuação {scored_agents[0]['score']}"
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
