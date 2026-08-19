"""Adapter: Grok (xAI)."""
ADAPTER = {
    "id": "grok",
    "name": "Grok (xAI)",
    "outputFormat": "markdown",
    "integrationType": "instructions-export-only",
    "apiEnvVar": "XAI_API_KEY",
    "limitations": "Exporta instrucoes para copia manual; API opcional via LLMClient.",
    "steps": "Instrucao de sistema.",
}
