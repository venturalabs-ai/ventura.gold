"""Adapter: Perplexity."""
ADAPTER = {
    "id": "perplexity",
    "name": "Perplexity",
    "outputFormat": "markdown",
    "integrationType": "instructions-export-only",
    "apiEnvVar": "PERPLEXITY_API_KEY",
    "limitations": "Exporta instrucoes para copia manual; API opcional via LLMClient.",
    "steps": "Incluir no inicio da conversa.",
}
