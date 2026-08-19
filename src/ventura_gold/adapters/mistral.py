"""Adapter: Mistral."""
ADAPTER = {
    "id": "mistral",
    "name": "Mistral",
    "outputFormat": "markdown",
    "integrationType": "instructions-export-only",
    "apiEnvVar": "MISTRAL_API_KEY",
    "limitations": "Exporta instrucoes para copia manual; API opcional via LLMClient.",
    "steps": "Instrucao de sistema.",
}
