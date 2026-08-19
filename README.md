# venture.gold

**100% Python Framework Portátil para Agentes e Skills de IA**

Venture Gold é um framework portátil para criar, testar, executar, revisar, documentar e exportar agentes e skills para diferentes ambientes de IA.

## Filosofia

- **Local-first**: Tudo que pode rodar localmente, roda localmente
- **Honestidade**: Adaptadores declaram requisitos e limitações de forma transparente
- **Sem referências a modelos base**: Saída 100% agnóstica de plataforma
- **Roteamento determinístico**: Correspondência por capacidades, sem chamadas a modelo
- **Exportação portátil**: Formato versionado para compatibilidade entre plataformas

## Recursos

- ✅ 100% Python — sem dependências Node.js/NPM
- ✅ Zero autenticação necessária para runtime local
- ✅ Compatível com Claude, ChatGPT, Grok, Copilot e principais plataformas de IA
- ✅ 100% funcional sem login/senha
- ✅ Nenhuma referência a modelo base na saída
- ✅ 10 adaptadores honestamente documentados
- ✅ Exportação de pacote portátil
- ✅ Roteamento determinístico por capacidades
- ✅ Suite de testes completa

## Quick Start

```bash
# Install
pip install venture.gold

# Type check / lint
python -m pytest tests/ --co -q

# Run the CLI
ventura-gold --prompt "planejar e revisar uma pesquisa"

# Doctor status
ventura-gold doctor

# Export portable package
ventura-gold export

# Validate the project
ventura-gold validate

# Test suite
python -m pytest tests/
```

## Supported Platforms (via Adapters)

1. Generic Instruction Agent (local, no auth)
2. Claude - Anthropic API (opcional)
3. ChatGPT - OpenAI API (opcional)
4. Grok - xAI API (opcional)
5. GitHub Copilot - VS Code integration (assinatura)
6. Gemini - Google API (opcional)
7. Mistral - Mistral AI API (opcional)
8. Perplexity - Perplexity AI API (opcional)
9. DeepSeek - DeepSeek API (opcional)
10. Qwen - Alibaba Cloud Qwen (opcional)

## CLI Commands

```bash
ventura-gold --prompt "..."          # Executar runtime com prompt
ventura-gold doctor                  # Verificar status do projeto
ventura-gold export                   # Exportar pacote portátil
ventura-gold validate                 # Validar projeto
ventura-gold list                     # Listar agentes e skills
```

## Documentation

- [`INSTALLATION.md`](docs/INSTALLATION.md) - Guia de instalação
- [`PORTABILITY.md`](docs/PORTABILITY.md) - Portabilidade e diferenças entre plataformas
- [`ARCHITECTURE.md`](docs/ARCHITECTURE.md) - Arquitetura e fluxo de dados
- [`SECURITY.md`](docs/SECURITY.md) - Modelo de ameaça e práticas de segredos
- [`ADAPTERS.md`](docs/ADAPTERS.md) - Matriz dos 10 adaptadores e limitações

## License

MIT - see [LICENSE](LICENSE) for details.

## Repository

[github.com/venturalabs-ai/ventura.gold](https://github.com/venturalabs-ai/ventura.gold)
