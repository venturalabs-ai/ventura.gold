"""Adapter: ChatGPT."""

ADAPTER = {
    "id": "chatgpt",
    "name": "ChatGPT",
    "outputFormat": "markdown",
    "integrationType": "instructions-export-only",
    "apiEnvVar": "OPENAI_API_KEY",
    "limitations": "Export/local first. API opcional se chave estiver no ambiente.",
}
