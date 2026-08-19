"""Adapter: GitHub Copilot — instructions-export-only."""

ADAPTER = {
    "id": "copilot",
    "name": "GitHub Copilot",
    "outputFormat": "markdown",
    "integrationType": "instructions-export-only",
    "apiEnvVar": None,
    "limitations": "Exporta instruções para cópia manual. Não publica automaticamente.",
    "steps": "Configurações → Copilot → Instruções personalizadas.",
}
