"""Skill: Gerador de Código."""

from __future__ import annotations

import re
from typing import Dict

from ventura_gold.core.llm_client import LLMClient


class CodeGeneratorSkill:
    def __init__(self, llm: LLMClient):
        self.llm = llm
        self.system_prompt = (
            "Você é um engenheiro de software sênior especialista em Python. "
            "Gere código limpo, tipado e documentado. Sem segredos hardcoded. "
            "Use bloco ```python ... ```."
        )

    def create_module(self, spec: str) -> Dict:
        resp = self.llm.generate(spec, self.system_prompt)
        return {
            "success": resp.success,
            "content": self._extract_code(resp.text),
            "explanation": self._strip_code(resp.text),
            "error": resp.error,
        }

    def improve(self, code: str, feedback: str = "") -> Dict:
        prompt = f"Melhore este código.\nFeedback: {feedback}\n\n```python\n{code}\n```"
        resp = self.llm.generate(prompt, self.system_prompt)
        return {
            "success": resp.success,
            "improved_code": self._extract_code(resp.text),
            "changes": self._strip_code(resp.text),
        }

    def _extract_code(self, text: str) -> str:
        m = re.search(r"```python\n(.*?)```", text or "", re.DOTALL)
        return m.group(1).strip() if m else (text or "")

    def _strip_code(self, text: str) -> str:
        return re.sub(r"```python.*?```", "", text or "", flags=re.DOTALL).strip()
