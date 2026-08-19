"""Adapter: Gemini."""

ADAPTER = {
    "id": "gemini",
    "name": "Gemini",
    "outputFormat": "markdown",
    "integrationType": "instructions-export-only",
    "apiEnvVar": "GEMINI_API_KEY",
    "limitations": "Export/local first. API opcional se chave estiver no ambiente.",
}
