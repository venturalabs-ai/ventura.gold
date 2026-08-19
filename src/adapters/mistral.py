"""Adapter: Mistral — instructions-export-only."""

ADAPTER = {
    "id": "mistral",
    "name": "Mistral",
    "outputFormat": "markdown",
    "integrationType": "instructions-export-only",
    "apiEnvVar": "MISTRAL_API_KEY",
    "limitations": "Exporta instruções para cópia manual. Não publica automaticamente.",
    "steps": "Campo de instrução de sistema → Colar.",
}
