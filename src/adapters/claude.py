"""Adapter: Claude (Anthropic) — instructions-export-only."""

ADAPTER = {
    "id": "claude",
    "name": "Claude (Anthropic)",
    "outputFormat": "markdown",
    "integrationType": "instructions-export-only",
    "apiEnvVar": "ANTHROPIC_API_KEY",
    "limitations": "Exporta instruções para cópia manual. Não publica automaticamente.",
    "steps": "Configurações → Instruções personalizadas → Colar.",
}
