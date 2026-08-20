# Ventura Infoproduto v2

Orquestrador completo com state machine para criação de infoprodutos lucrativos e escaláveis.

## Pipeline

```
DRAFT
  → niche_analysis        → NICHO_DEFINIDO
  → product_structure     → ESTRUTURA_CRIADA
  → sales_copy            → COPY_VSL_GERADA
  → ads_creation          → ANUNCIOS_CRIADOS
  → compliance            → COMPLIANCE_REVISADO
  → bilingual / source_validation / niche_ranking / qa / observability
  → PUBLISHED
```

## Uso rápido

```python
from ventura_gold.infoproduto import VenturaOrchestrator, Language

orch = VenturaOrchestrator()
ctx = orch.start_session(user_id="user123", language=Language.PT_BR)

# Preencher campos do contexto (nicho, dor, etc.) ou responder perguntas
ctx.nicho = "emagrecimento"
ctx.dor_principal = "não consegue manter o peso após dietas"
# ...

ctx = orch.run_full_pipeline(ctx)
files = orch.export_deliverables(ctx, output_dir="./entregaveis")
```

## CLI

```bash
python -m ventura_gold.infoproduto.orchestrator --user-id u1 --full --export ./out
```

## Skills (JSON)

- `niche_analysis_skill`
- `product_structure_skill`
- `sales_copy_skill`
- `ads_creation_skill`
- `compliance_skill`
- `bilingual_content_skill`
- `source_validation_ranking_skill`
