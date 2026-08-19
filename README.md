# ventura.gold

**Agente de Repositório Automatizado — 100% Python, local-first**

Framework para analisar repositórios, montar planos de agentes/skills, exportar pacotes portáteis e (opcionalmente) integrar LLMs.

> **Local-first by design:** execução offline, sem autenticação obrigatória. APIs de IA permanecem opcionais.

## Install

```bash
pip install -e ".[dev]"
```

## Commands

```bash
ventura-gold doctor
ventura-gold list
ventura-gold validate
ventura-gold export
ventura-gold run --prompt "planejar refatoração"
ventura-gold repo scan
ventura-gold repo generate-code --spec "módulo de cache LRU"
ventura-gold repo generate-tests --file src/ventura_gold/core/router.py
```

## Architecture

- `core/` — registry, router, runtime, exporter, validator, llm_client, context
- `mcp/` — Git + filesystem tool servers
- `skills/` — repository analyst, code generator, test builder
- `adapters/` — platform adapters (export + optional API)
- `cli.py` — Typer CLI

## License

MIT
