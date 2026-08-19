"""Intelligent context management — prioritizes chunks within a token budget."""
from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class ContextChunk:
    source: str
    content: str
    priority: int  # 1 = highest
    tokens: int = 0

    def __post_init__(self) -> None:
        if not self.tokens:
            self.tokens = max(1, len(self.content) // 4)


class ContextManager:
    def __init__(self, model: str = "generic", max_tokens: int = 120_000):
        self.model = model
        self.max_tokens = max_tokens
        self._encoder = None
        try:
            import tiktoken  # optional

            self._encoder = tiktoken.encoding_for_model(model) if model != "generic" else tiktoken.get_encoding("cl100k_base")
        except Exception:
            self._encoder = None

    def count_tokens(self, text: str) -> int:
        if self._encoder is not None:
            return len(self._encoder.encode(text or ""))
        return max(1, len(text or "") // 4)

    def optimize(self, chunks: List[ContextChunk]) -> str:
        ordered = sorted(chunks, key=lambda c: c.priority)
        selected: list[ContextChunk] = []
        total = 0
        for chunk in ordered:
            t = chunk.tokens or self.count_tokens(chunk.content)
            if total + t <= self.max_tokens:
                selected.append(chunk)
                total += t
            else:
                break
        return "\n\n---\n\n".join(f"### {c.source}\n{c.content}" for c in selected)
