"""Adapter: Claude (Anthropic)."""
ADAPTER = {
    "id": "claude",
    "name": "Claude (Anthropic)",
    "outputFormat": "markdown",
    "integrationType": "instructions-export-only",
    "apiEnvVar": "ANTHROPIC_API_KEY",
    "limitations": "Exporta instrucoes para copia manual; API opcional via LLMClient.",
    "steps": "Instrucoes personalizadas.",
}
