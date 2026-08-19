"""Adapter: DeepSeek — instructions-export-only."""

ADAPTER = {
    "id": "deepseek",
    "name": "DeepSeek",
    "outputFormat": "markdown",
    "integrationType": "instructions-export-only",
    "apiEnvVar": "DEEPSEEK_API_KEY",
    "limitations": "Exporta instruções para cópia manual. Não publica automaticamente.",
    "steps": "Campo de instrução de sistema → Colar.",
}
