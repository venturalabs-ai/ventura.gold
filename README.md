# ventura.gold

**Agente de repositório automatizado — 100% Python, local-first.**

> Offline by default. Optional LLM APIs. MCP-style local tools for Git and filesystem.

## Features

- Local-first runtime (no login required)
- Deterministic agent/skill routing
- Repository scan (`ventura-gold repo scan`)
- Optional multi-provider LLM client
- Portable export package
- CI with tests + secret pattern scan
- **Novo: Ecossistema completo de Infoprodutos** (estratégia → conteúdo → copy → página → materiais → ads compliance)

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
├── agents/                    # .md definitions
│   └── ventura_infoproduto.md # Orquestrador de infoprodutos
├── skills/
│   ├── repository/            # scan & analysis
│   ├── codegen/               # code generation
│   ├── testing/               # test generation
│   ├── docs/                  # documentation
│   ├── review/                # audit & review
│   ├── infoproduto_criacao/   # Estratégia do produto
│   ├── infoproduto_conteudo/  # Conteúdo didático
│   ├── copywriting/           # Frameworks e componentes de copy
│   ├── pagina_vendas/         # Página HTML + VSL
│   ├── materiais_vendas/      # E-mail, WhatsApp, webinar, posts
│   ├── ads_compliance/        # Criativos Meta/Google + compliance
│   └── infoproduto/           # Orquestrador Python
├── adapters/                  # 10 LLM adapters
├── mcp/                       # Git + filesystem tools
├── core/
└── cli.py
```

## Ecossistema Infoproduto

Pipeline completo para criar infoprodutos de alta conversão com compliance:

1. `infoproduto_criacao` → Estratégia (promessa, mecanismo, módulos, oferta)
2. `infoproduto_conteudo` → Roteiros, exercícios, PDFs e bônus
3. `copywriting` → AIDA, PAS, StoryBrand + headlines, bullets, FAQ
4. `pagina_vendas` → HTML completo + VSL + seções de conversão
5. `materiais_vendas` → Sequências de e-mail, WhatsApp, webinar, posts
6. `ads_compliance` → Criativos Meta + Google com validação automática
7. `review` → Auditoria final

Documentação detalhada: [docs/INFOPRODUTO_ECOSYSTEM.md](docs/INFOPRODUTO_ECOSYSTEM.md)

## License

MIT (c) Ventura Labs AI
