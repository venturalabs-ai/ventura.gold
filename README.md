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
ventura-gold repo docs
ventura-gold repo review
ventura-gold repo generate-code --spec "modulo utilitario X"
ventura-gold repo generate-tests --file src/ventura_gold/core/router.py
```

## Package layout

```text
src/ventura_gold/
├── agents/           # .md definitions
├── skills/
│   ├── repository/   # scan & analysis
│   ├── codegen/      # code generation
│   ├── testing/      # test generation
│   ├── docs/         # documentation
│   └── review/       # audit & review
├── adapters/         # 10 LLM adapters
├── mcp/              # Git + filesystem tools
├── core/
└── cli.py
```

## License

MIT (c) Ventura Labs AI
