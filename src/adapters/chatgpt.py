"""Adapter: ChatGPT (OpenAI) — instructions-export-only."""

ADAPTER = {
    "id": "chatgpt",
    "name": "ChatGPT (OpenAI)",
    "outputFormat": "markdown",
    "integrationType": "instructions-export-only",
    "apiEnvVar": "OPENAI_API_KEY",
    "limitations": "Exporta instruções para cópia manual. Não publica automaticamente.",
    "steps": "Configurações → Instruções personalizadas → Colar.",
}
