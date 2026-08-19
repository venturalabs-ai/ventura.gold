"""Adapter: Gemini (Google) — instructions-export-only."""

ADAPTER = {
    "id": "gemini",
    "name": "Gemini (Google)",
    "outputFormat": "markdown",
    "integrationType": "instructions-export-only",
    "apiEnvVar": "GEMINI_API_KEY",
    "limitations": "Exporta instruções para cópia manual. Não publica automaticamente.",
    "steps": "Configurações → Instruções do assistente → Colar.",
}
