# ventura.gold

**Agente de repositorio automatizado — 100% Python, local-first.**

> Offline by default. Optional LLM APIs. MCP-style local tools for Git and filesystem.

## Features

- Local-first runtime (no login required)
- Deterministic agent/skill routing
- Repository scan (`ventura-gold repo scan`)
- Optional multi-provider LLM client
- Portable export package
- CI with tests + secret pattern scan

## Install

```bash
git clone https://github.com/venturalabs-ai/ventura.gold.git
cd ventura.gold
pip install -e ".[dev]"
```

## Commands

```bash
ventura-gold doctor
ventura-gold list
ventura-gold validate
ventura-gold export
ventura-gold run --prompt "planejar analise do repositorio"
ventura-gold repo scan
ventura-gold repo generate-code --spec "modulo utilitario X"
ventura-gold repo generate-tests --file src/ventura_gold/core/router.py
```

## License

MIT (c) Ventura Labs AI
