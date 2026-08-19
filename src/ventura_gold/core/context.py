"""Gestão de contexto — otimiza janela de conteúdo sem dependência pesada."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class ContextChunk:
    source: str
    content: str
    priority: int  # 1 = mais importante
    tokens: int = 0

    def __post_init__(self) -> None:
        if not self.tokens:
            self.tokens = max(1, len(self.content) // 4)


class ContextManager:
    def __init__(self, max_tokens: int = 120_000):
        self.max_tokens = max_tokens

    def count_tokens(self, text: str) -> int:
        return max(1, len(text or "") // 4)

    def optimize(self, chunks: List[ContextChunk]) -> str:
        ordered = sorted(chunks, key=lambda c: c.priority)
        selected: List[ContextChunk] = []
        total = 0
        for chunk in ordered:
            if total + chunk.tokens <= self.max_tokens:
                selected.append(chunk)
                total += chunk.tokens
        return "\n\n---\n\n".join(f"### {c.source}\n{c.content}" for c in selected)
