"""Adapter: DeepSeek."""

ADAPTER = {
    "id": "deepseek",
    "name": "DeepSeek",
    "outputFormat": "markdown",
    "integrationType": "instructions-export-only",
    "apiEnvVar": "DEEPSEEK_API_KEY",
    "limitations": "Export/local first. API opcional se chave estiver no ambiente.",
}
