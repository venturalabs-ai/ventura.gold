"""Adapter: DeepSeek."""
ADAPTER = {
    "id": "deepseek",
    "name": "DeepSeek",
    "outputFormat": "markdown",
    "integrationType": "instructions-export-only",
    "apiEnvVar": "DEEPSEEK_API_KEY",
    "limitations": "Exporta instrucoes para copia manual; API opcional via LLMClient.",
    "steps": "Instrucao de sistema.",
}
