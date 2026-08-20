# Ecossistema Infoproduto — Ventura Gold

Pipeline completo e unificado para criação de infoprodutos de alta conversão, com compliance rigoroso.

## Visão Geral

O **Ventura Infoproduto** é um agente orquestrador + 6 skills especializadas que transformam um briefing em um pacote completo de lançamento:

```
Briefing
   ↓
1. infoproduto_criacao     → Estratégia (promessa, mecanismo, módulos, oferta)
   ↓
2. infoproduto_conteudo    → Conteúdo (aulas, PDFs, exercícios, bônus)
   ↓
3. copywriting             → Frameworks (AIDA, PAS, StoryBrand...) + componentes reutilizáveis
   ↓
4. pagina_vendas           → HTML completo + VSL + seções de alta conversão
   ↓
5. materiais_vendas        → E-mails, WhatsApp, carta PDF, webinar, posts, slides
   ↓
6. ads_compliance          → Criativos Meta + Google + relatório de compliance
   ↓
7. review                  → Revisão final de consistência, compliance e qualidade
```

## Skills Incluídas

| Skill                  | ID                     | Função principal                          |
|------------------------|------------------------|-------------------------------------------|
| Criação Estratégica    | `infoproduto_criacao`  | Base do produto e oferta                  |
| Conteúdo               | `infoproduto_conteudo` | Roteiros, exercícios e materiais didáticos|
| Copywriting            | `copywriting`          | Headlines, bullets, frameworks, FAQ       |
| Página de Vendas       | `pagina_vendas`        | HTML completo + VSL + SEO                 |
| Materiais de Vendas    | `materiais_vendas`     | E-mail, WhatsApp, webinar, posts          |
| Ads Compliance         | `ads_compliance`       | Criativos + validação Meta/Google         |

## Agente

- **ID**: `ventura_infoproduto`
- **Arquivo**: `src/ventura_gold/agents/ventura_infoproduto.md`
- **Orquestrador Python**: `src/ventura_gold/skills/infoproduto/orchestrator.py`

## Princípios do Ecossistema

1. **Consistência da promessa** — a mesma promessa_principal flui por todos os assets.
2. **Compliance first** — regras de Meta e Google são aplicadas antes da geração final.
3. **Sem claims absolutos** — nenhum "garantido", "milagre" ou promessa de resultado financeiro/saúde.
4. **Prova real apenas** — placeholders obrigatórios quando não houver depoimento real.
5. **Urgência real** — apenas vagas limitadas por suporte, bônus por tempo ou turma fechada.
6. **Mobile-first e SEO** — páginas e criativos nascem otimizados.

## Como usar

```bash
# Via CLI (quando o runtime estiver conectado)
ventura-gold run --prompt "Crie um infoproduto completo de [nicho] para [avatar]"

# Ou importe o orquestrador
from ventura_gold.skills.infoproduto import VenturaInfoproduto

agent = VenturaInfoproduto(runtime=seu_runtime)
resultado = agent.run_pipeline(briefing)
```

## Estrutura de Arquivos

```
src/ventura_gold/
├── agents/
│   └── ventura_infoproduto.md
└── skills/
    ├── infoproduto_criacao/SKILL.md
    ├── infoproduto_conteudo/SKILL.md
    ├── copywriting/SKILL.md
    ├── pagina_vendas/SKILL.md
    ├── materiais_vendas/SKILL.md
    ├── ads_compliance/SKILL.md
    └── infoproduto/
        ├── __init__.py
        └── orchestrator.py
```

---

**Ventura Labs AI** — Ecossistema perfeito de criação de infoprodutos.
