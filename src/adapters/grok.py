"""Adapter: Grok (xAI) — instructions-export-only."""

ADAPTER = {
    "id": "grok",
    "name": "Grok (xAI)",
    "outputFormat": "markdown",
    "integrationType": "instructions-export-only",
    "apiEnvVar": "XAI_API_KEY",
    "limitations": "Exporta instruções para cópia manual. Não publica automaticamente.",
    "steps": "Configurações → Instrução de sistema → Colar.",
}
