"""Adapter: ChatGPT (OpenAI)."""
ADAPTER = {
    "id": "chatgpt",
    "name": "ChatGPT (OpenAI)",
    "outputFormat": "markdown",
    "integrationType": "instructions-export-only",
    "apiEnvVar": "OPENAI_API_KEY",
    "limitations": "Exporta instrucoes para copia manual; API opcional via LLMClient.",
    "steps": "Instrucoes personalizadas.",
}
