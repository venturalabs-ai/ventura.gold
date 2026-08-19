"""Skill: Construtor de Testes."""

from __future__ import annotations

import re
from typing import Dict

from ventura_gold.core.llm_client import LLMClient


class TestBuilderSkill:
    def __init__(self, llm: LLMClient):
        self.llm = llm
        self.system = (
            "Você é especialista em testes Python com pytest. "
            "Gere testes determinísticos com casos de sucesso e falha."
        )

    def generate_tests(self, source_code: str, module_name: str = "module") -> Dict:
        prompt = (
            f"Gere testes pytest para o módulo {module_name}:\n\n"
            f"```python\n{source_code}\n```"
        )
        resp = self.llm.generate(prompt, self.system)
        return {
            "success": resp.success,
            "test_code": self._extract_code(resp.text),
            "explanation": self._strip_code(resp.text),
            "error": resp.error,
        }

    def _extract_code(self, text: str) -> str:
        m = re.search(r"```python\n(.*?)```", text or "", re.DOTALL)
        return m.group(1).strip() if m else ""

    def _strip_code(self, text: str) -> str:
        return re.sub(r"```python.*?```", "", text or "", flags=re.DOTALL).strip()
