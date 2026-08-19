"""Adapter: Perplexity."""

ADAPTER = {
    "id": "perplexity",
    "name": "Perplexity",
    "outputFormat": "markdown",
    "integrationType": "instructions-export-only",
    "apiEnvVar": "PERPLEXITY_API_KEY",
    "limitations": "Export/local first. API opcional se chave estiver no ambiente.",
}
