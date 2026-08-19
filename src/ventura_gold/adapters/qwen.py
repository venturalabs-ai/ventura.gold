"""Adapter: Qwen."""

ADAPTER = {
    "id": "qwen",
    "name": "Qwen",
    "outputFormat": "markdown",
    "integrationType": "instructions-export-only",
    "apiEnvVar": "QWEN_API_KEY",
    "limitations": "Export/local first. API opcional se chave estiver no ambiente.",
}
