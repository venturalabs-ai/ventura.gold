"""Adapter: Qwen — instructions-export-only."""

ADAPTER = {
    "id": "qwen",
    "name": "Qwen",
    "outputFormat": "markdown",
    "integrationType": "instructions-export-only",
    "apiEnvVar": "QWEN_API_KEY",
    "limitations": "Exporta instruções para cópia manual. Não publica automaticamente.",
    "steps": "Campo de prompt de sistema → Colar.",
}
