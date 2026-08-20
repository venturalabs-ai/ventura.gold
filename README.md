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
- **Ecossistema Infoproduto v2** — state machine completa (nicho → estrutura → copy/VSL → ads → compliance → bilingual → QA)

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
│   └── ventura_infoproduto.md
├── infoproduto/               # ★ Ecossistema v2 (state machine)
│   ├── orchestrator.py        # VenturaOrchestrator + todos os agentes
│   ├── agents/                # versões refinadas (niche, product structure)
│   ├── skills/                # skill JSONs de domínio
│   └── README.md
├── skills/
│   ├── repository/, codegen/, testing/, docs/, review/
│   ├── infoproduto_criacao/, infoproduto_conteudo/, copywriting/
│   ├── pagina_vendas/, materiais_vendas/, ads_compliance/
│   └── infoproduto/           # wrapper de compatibilidade v1→v2
├── adapters/                  # 10 LLM adapters
├── mcp/                       # Git + filesystem tools
├── core/
└── cli.py
```

## Ecossistema Infoproduto v2

```python
from ventura_gold.infoproduto import VenturaOrchestrator, Language

orch = VenturaOrchestrator()
ctx = orch.start_session(user_id="user123", language=Language.PT_BR)
ctx.nicho = "emagrecimento"
ctx.dor_principal = "..."
ctx = orch.run_full_pipeline(ctx)
orch.export_deliverables(ctx, "./entregaveis")
```

**Pipeline (FlowState):**

1. `niche_analysis` → NICHO_DEFINIDO  
2. `product_structure` → ESTRUTURA_CRIADA  
3. `sales_copy` → COPY_VSL_GERADA  
4. `ads_creation` → ANUNCIOS_CRIADOS  
5. `compliance` → COMPLIANCE_REVISADO  
6. bilingual / source_validation / niche_ranking / qa / observability → PUBLISHED  

Skills declarativas em `src/ventura_gold/skills/` (v1) continuam disponíveis.  
Documentação: [docs/INFOPRODUTO_ECOSYSTEM.md](docs/INFOPRODUTO_ECOSYSTEM.md)

## License

MIT (c) Ventura Labs AI
