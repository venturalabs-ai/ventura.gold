"""Cliente LLM unificado — API opcional; fallback local sem chave."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class LLMResponse:
    text: str
    model: str
    provider: str
    tokens_used: int = 0
    success: bool = True
    error: Optional[str] = None


class LLMClient:
    """Interface unificada. Sem chave = modo local (não chama API)."""

    PROVIDERS = {
        "claude": ("ANTHROPIC_API_KEY", "https://api.anthropic.com/v1/messages"),
        "chatgpt": ("OPENAI_API_KEY", "https://api.openai.com/v1/chat/completions"),
        "openai": ("OPENAI_API_KEY", "https://api.openai.com/v1/chat/completions"),
        "gemini": ("GEMINI_API_KEY", None),
        "mistral": ("MISTRAL_API_KEY", "https://api.mistral.ai/v1/chat/completions"),
        "deepseek": ("DEEPSEEK_API_KEY", "https://api.deepseek.com/v1/chat/completions"),
        "qwen": ("QWEN_API_KEY", "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"),
        "perplexity": ("PERPLEXITY_API_KEY", "https://api.perplexity.ai/chat/completions"),
        "grok": ("XAI_API_KEY", "https://api.x.ai/v1/chat/completions"),
        "generic": (None, None),
    }

    def __init__(self, provider: str = "generic", model: Optional[str] = None):
        self.provider = (provider or "generic").lower()
        env_name, endpoint = self.PROVIDERS.get(self.provider, (None, None))
        self.endpoint = endpoint
        self.api_key = os.getenv(env_name) if env_name else None
        self.model = model or self._default_model()
        self.mode = "api" if self.api_key and self.endpoint else "local"

    def _default_model(self) -> str:
        defaults = {
            "claude": "claude-3-5-sonnet-20241022",
            "chatgpt": "gpt-4o",
            "openai": "gpt-4o",
            "gemini": "gemini-2.0-flash",
            "mistral": "mistral-large-latest",
            "deepseek": "deepseek-chat",
            "qwen": "qwen-max",
            "perplexity": "llama-3.1-sonar-large-128k-online",
            "grok": "grok-2-latest",
        }
        return defaults.get(self.provider, "instruction-model")

    def generate(self, prompt: str, system_prompt: str = "", **kwargs: Any) -> LLMResponse:
        if self.mode == "local":
            text = (
                "[MODO LOCAL — sem chamada à API]\n\n"
                f"{system_prompt}\n\n{prompt}" if system_prompt else f"[MODO LOCAL]\n\n{prompt}"
            )
            return LLMResponse(
                text=text,
                model=self.model,
                provider=self.provider,
                success=False,
                error="no_api_key",
            )

        try:
            import httpx

            headers = self._headers()
            payload = self._payload(prompt, system_prompt, **kwargs)
            with httpx.Client(timeout=120.0) as client:
                resp = client.post(self.endpoint, headers=headers, json=payload)
                resp.raise_for_status()
                return self._parse_response(resp.json())
        except Exception as e:
            return LLMResponse(
                text="",
                model=self.model,
                provider=self.provider,
                success=False,
                error=str(e),
            )

    def _headers(self) -> Dict[str, str]:
        if self.provider == "claude":
            return {
                "x-api-key": self.api_key or "",
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            }
        return {"Authorization": f"Bearer {self.api_key}", "content-type": "application/json"}

    def _payload(self, prompt: str, system: str, **kwargs: Any) -> Dict[str, Any]:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        if self.provider == "claude":
            body: Dict[str, Any] = {
                "model": self.model,
                "max_tokens": kwargs.pop("max_tokens", 4096),
                "messages": messages,
            }
            body.update(kwargs)
            return body
        body = {"model": self.model, "messages": messages}
        body.update(kwargs)
        return body

    def _parse_response(self, data: Dict[str, Any]) -> LLMResponse:
        if self.provider == "claude":
            content = "".join(block.get("text", "") for block in data.get("content", []))
        else:
            content = data["choices"][0]["message"]["content"]
        usage = data.get("usage") or {}
        tokens = usage.get("total_tokens", 0)
        return LLMResponse(
            text=content,
            model=self.model,
            provider=self.provider,
            tokens_used=tokens,
            success=True,
        )
