"""Adapter: Qwen."""
ADAPTER = {
    "id": "qwen",
    "name": "Qwen",
    "outputFormat": "markdown",
    "integrationType": "instructions-export-only",
    "apiEnvVar": "QWEN_API_KEY",
    "limitations": "Exporta instrucoes para copia manual; API opcional via LLMClient.",
    "steps": "Prompt de sistema.",
}
