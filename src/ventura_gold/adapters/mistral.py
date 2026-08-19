"""Adapter: Mistral."""

ADAPTER = {
    "id": "mistral",
    "name": "Mistral",
    "outputFormat": "markdown",
    "integrationType": "instructions-export-only",
    "apiEnvVar": "MISTRAL_API_KEY",
    "limitations": "Export/local first. API opcional se chave estiver no ambiente.",
}
