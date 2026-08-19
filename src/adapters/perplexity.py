"""Adapter: Perplexity — instructions-export-only."""

ADAPTER = {
    "id": "perplexity",
    "name": "Perplexity",
    "outputFormat": "markdown",
    "integrationType": "instructions-export-only",
    "apiEnvVar": "PERPLEXITY_API_KEY",
    "limitations": "Exporta instruções para cópia manual. Não publica automaticamente.",
    "steps": "Incluir instrução no início da conversa.",
}
