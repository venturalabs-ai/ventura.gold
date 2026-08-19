"""Adapter: Claude."""

ADAPTER = {
    "id": "claude",
    "name": "Claude",
    "outputFormat": "markdown",
    "integrationType": "instructions-export-only",
    "apiEnvVar": "ANTHROPIC_API_KEY",
    "limitations": "Export/local first. API opcional se chave estiver no ambiente.",
}
