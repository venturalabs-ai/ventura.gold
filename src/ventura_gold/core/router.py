"""Deterministic capability-based routing."""
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


def score_candidate(candidate: Dict[str, Any], prompt: str) -> int:
    np = normalize_text(prompt)
    nn = normalize_text(candidate.get("name", ""))
    nd = normalize_text(candidate.get("description", ""))
    caps = [normalize_text(str(c)) for c in candidate.get("capabilities", [])]
    score = 0
    words = [w for w in np.split() if len(w) > 2]
    if np and np == nn:
        score += 100
    elif np and np in nn:
        score += 70
    else:
        score += sum(15 for w in words if w in nn.split())
    if np and np in nd:
        score += 50
    else:
        score += sum(10 for w in words if w in nd.split())
    for cap in caps:
        if np and np in cap:
            score += 30
        else:
            score += sum(5 for w in words if w in cap.split())
    return score


def route(
    prompt: str,
    agents: Optional[List[Dict[str, Any]]] = None,
    skills: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    agents = agents or []
    skills = skills or []
    scored_a = sorted(
        ({"item": a, "score": score_candidate(a, prompt)} for a in agents),
        key=lambda x: (-x["score"], x["item"].get("id", "")),
    )
    scored_s = sorted(
        ({"item": s, "score": score_candidate(s, prompt)} for s in skills),
        key=lambda x: (-x["score"], x["item"].get("id", "")),
    )
    best = scored_a[0] if scored_a else None
    selected_skills = [s["item"] for s in scored_s if s["score"] >= 12]
    if best and best["score"] > 0:
        agent = best["item"]
        reason = f"Melhor correspondência com pontuação {best['score']}"
    elif scored_a:
        orch = next((s for s in scored_a if s["item"].get("id") == "orchestrator"), scored_a[0])
        agent = orch["item"]
        reason = "Nenhuma correspondência forte — usando agente padrão"
    else:
        agent = None
        reason = "Nenhum agente registrado"
    return {
        "agent": agent,
        "skills": selected_skills,
        "scores": [{"id": s["item"].get("id"), "score": s["score"]} for s in scored_a],
        "reason": reason,
    }
