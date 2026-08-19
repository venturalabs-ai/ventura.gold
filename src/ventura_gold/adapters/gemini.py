"""Adapter: Gemini (Google)."""
ADAPTER = {
    "id": "gemini",
    "name": "Gemini (Google)",
    "outputFormat": "markdown",
    "integrationType": "instructions-export-only",
    "apiEnvVar": "GEMINI_API_KEY",
    "limitations": "Exporta instrucoes para copia manual; API opcional via LLMClient.",
    "steps": "Instrucoes do assistente.",
}
