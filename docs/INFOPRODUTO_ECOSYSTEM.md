# Ecossistema Infoproduto — Ventura Gold v2

Pipeline completo com **state machine** para criação de infoprodutos de alta conversão, bilingual (PT-BR / EN-US), compliance Meta/Google e exportação de entregáveis.

## Arquitetura

```
src/ventura_gold/infoproduto/
├── orchestrator.py          # VenturaOrchestrator + BaseAgent + todos os agentes
├── agents/
│   ├── niche_analysis_agent.py      # versão refinada
│   └── product_structure_agent.py   # versão refinada
├── skills/                  # definições JSON de domínio
│   ├── niche_analysis_skill.json
│   ├── product_structure_skill.json
│   ├── sales_copy_skill.json
│   ├── ads_creation_skill.json
│   ├── compliance_skill.json
│   ├── bilingual_content_skill.json
│   └── source_validation_ranking_skill.json
└── README.md
```

## FlowState

| Estado | Significado |
|--------|-------------|
| `DRAFT` | Sessão iniciada |
| `NICHO_DEFINIDO` | Nicho, dor e audiência definidos + ranking |
| `ESTRUTURA_CRIADA` | Nome, promessa, módulos, bônus, garantia |
| `COPY_VSL_GERADA` | Headline + VSL + oferta |
| `ANUNCIOS_CRIADOS` | Meta + Google ads (5 variações) |
| `COMPLIANCE_REVISADO` | Validação de claims e regras de plataforma |
| `PUBLISHED` | Pipeline concluído |

## Agentes

| Agente | Função |
|--------|--------|
| NicheAnalysisAgent | Nicho, audiência, dor, ranking BR/US |
| ProductStructureAgent | Nome, promessa, módulos, bônus, garantia |
| SalesCopyAgent | Headline, VSL, oferta (AIDA/PAS) |
| AdsCreationAgent | 5 variações Meta + Google |
| ComplianceAgent | Regras saúde/finanças/geral Meta & Google |
| BilingualContentAgent | PT-BR ↔ EN-US com adaptação cultural |
| SourceValidationAgent | Credibilidade de fontes |
| NicheRankingAgent | Ranking visual de mercado |
| QATestAgent | QA de campos, links, formatação |
| ObservabilityAgent | Métricas de execução |
| RepositoryAuditAgent | Auditoria de repositório |

## Uso

```python
from ventura_gold.infoproduto import VenturaOrchestrator, Language, FlowState

orch = VenturaOrchestrator(config_path=None)
ctx = orch.start_session("user-001", Language.PT_BR)

# Preencher briefing
ctx.nicho = "finanças pessoais"
ctx.sub_nicho = "investimento para iniciantes"
ctx.audiencia_primaria = "30-45 anos, CLT, sem experiência"
ctx.dor_principal = "dinheiro some no fim do mês e não sabe por onde começar"
ctx.transformacao_desejada = "ter um plano simples e renda passiva em 12 meses"

ctx = orch.run_full_pipeline(ctx)
print(ctx.current_state)  # FlowState.PUBLISHED

files = orch.export_deliverables(ctx, "./out")
# 01_briefing.md, 02_estrutura.md, 03_vsl.md, 04_anuncios.md,
# 05_relatorio_compliance.md, 06_ranking_nicho.md, ...
```

## CLI

```bash
python -m ventura_gold.infoproduto.orchestrator \
  --user-id demo \
  --language pt-BR \
  --full \
  --export ./entregaveis
```

## Compatibilidade v1

O módulo `ventura_gold.skills.infoproduto.VenturaInfoproduto` continua disponível e, quando possível, delega para o `VenturaOrchestrator` v2.

Skills declarativas em Markdown (`infoproduto_criacao`, `copywriting`, `pagina_vendas`, etc.) permanecem para o runtime de routing do ventura.gold.

---

**Ventura Labs AI** — Ecossistema de criação de infoprodutos.
