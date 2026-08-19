"""Adapter: Grok."""

ADAPTER = {
    "id": "grok",
    "name": "Grok",
    "outputFormat": "markdown",
    "integrationType": "instructions-export-only",
    "apiEnvVar": "XAI_API_KEY",
    "limitations": "Export/local first. API opcional se chave estiver no ambiente.",
}
