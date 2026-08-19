"""Skill: code generator — uses LLM client with local fallback."""
from __future__ import annotations

import re
from typing import Any, Dict

from ventura_gold.core.llm_client import LLMClient


class CodeGeneratorSkill:
    def __init__(self, llm: LLMClient):
        self.llm = llm
        self.system_prompt = (
            "Voce e um engenheiro de software senior especialista em Python. "
            "Codigo limpo, tipado, documentado, sem segredos hardcoded."
        )

    async def create_module(self, spec: str) -> Dict[str, Any]:
        resp = await self.llm.generate(spec, self.system_prompt)
        return {
            "success": resp.success,
            "content": self._extract_code(resp.text),
            "explanation": self._strip_code(resp.text),
            "error": resp.error,
            "mode": resp.mode,
        }

    def _extract_code(self, text: str) -> str:
        m = re.search(r"```python\n(.*?)```", text or "", re.DOTALL)
        return m.group(1).strip() if m else (text or "")

    def _strip_code(self, text: str) -> str:
        return re.sub(r"```python.*?```", "", text or "", flags=re.DOTALL).strip()
