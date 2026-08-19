"""Skill: test builder — generates pytest suites via LLM client."""
from __future__ import annotations

import re
from typing import Any, Dict

from ventura_gold.core.llm_client import LLMClient


class TestBuilderSkill:
    def __init__(self, llm: LLMClient):
        self.llm = llm
        self.system = (
            "Voce e especialista em testes Python com pytest. "
            "Gere testes deterministicos com casos de sucesso e falha."
        )

    async def generate_tests(self, source_code: str, module_name: str = "module") -> Dict[str, Any]:
        prompt = f"""Gere arquivo de testes para este codigo:

# Modulo: {module_name}

```python
{source_code}
```

Use pytest. Inclua docstrings e casos de borda."""
        resp = await self.llm.generate(prompt, self.system)
        return {
            "success": resp.success,
            "test_code": self._extract_code(resp.text),
            "explanation": self._strip_code(resp.text),
            "mode": resp.mode,
            "error": resp.error,
        }

    def _extract_code(self, text: str) -> str:
        m = re.search(r"```python\n(.*?)```", text or "", re.DOTALL)
        return m.group(1).strip() if m else ""

    def _strip_code(self, text: str) -> str:
        return re.sub(r"```python.*?```", "", text or "", flags=re.DOTALL).strip()
