"""Adapter: GitHub Copilot."""
ADAPTER = {
    "id": "copilot",
    "name": "GitHub Copilot",
    "outputFormat": "markdown",
    "integrationType": "instructions-export-only",
    "apiEnvVar": None,
    "limitations": "Exporta instrucoes para copia manual; API opcional via LLMClient.",
    "steps": "Copilot instructions.",
}
