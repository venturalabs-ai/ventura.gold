"""Adapter: Generico."""
ADAPTER = {
    "id": "generic",
    "name": "Generico",
    "outputFormat": "markdown",
    "integrationType": "instructions-export-only",
    "apiEnvVar": None,
    "limitations": "Exporta instrucoes para copia manual; API opcional via LLMClient.",
    "steps": "Copiar e colar nas instrucoes de sistema.",
}
