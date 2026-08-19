# Adaptadores e Plataformas Suportadas

## Matriz de capacidades

| Plataforma  | Instrução automática | API disponível | Exige conta      |
|-------------|----------------------|----------------|------------------|
| Claude      | Manual               | Opcional       | Apenas API       |
| ChatGPT     | Manual               | Opcional       | Apenas API       |
| Grok        | Manual               | Opcional       | Sim (API)        |
| Copilot     | Manual               | Não pública    | Assinatura       |
| Gemini      | Manual               | Opcional       | Apenas API       |
| Mistral     | Manual               | Opcional       | Apenas API       |
| Perplexity  | No prompt            | Opcional       | Apenas API       |
| DeepSeek    | Manual               | Opcional       | Apenas API       |
| Qwen        | Manual               | Opcional       | Apenas API       |
| Genérico    | Copiar e colar       | Não            | Não              |

## Legenda

- **Manual**: o adaptador gera o texto — você copia e cola nas configurações da IA
- **Opcional**: a API existe e pode ser usada com chave, mas **não** é obrigatória
- **Não disponível publicamente**

Todos os adaptadores implementam a mesma interface declarativa (`id`, `name`, `outputFormat`, `integrationType`, `apiEnvVar`, `limitations`, `steps`).
