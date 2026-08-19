# Arquitetura do Sistema

## Princípios de design

- **Local-first:** tudo que pode rodar localmente, roda localmente
- **Sem bloqueio por padrão:** avisos não interrompem funcionamento
- **Determinístico:** mesma entrada = mesmo roteamento
- **Extensível:** basta adicionar arquivos `.json` para criar agentes e skills
- **Sem dependências pesadas:** usar APIs nativas do Python

## Fluxo de execução

```
Entrada do Usuário
│
▼
Carregar Registro ── ler arquivos .json
│
▼
Roteamento ─────── pontuar correspondências
│
▼
Montar Plano ───── agrupar instruções
│
▼
Gerar Saída ────── JSON + instruções
│
▼
Adaptador ───────── formatar por plataforma (opcional)
```

## Módulos principais

- **frontmatter.py** — Parser leve de metadados sem dependências externas
- **registry.py** — Descoberta automática de agentes e skills
- **router.py** — Pontuação e seleção determinística
- **runtime.py** — Montagem de plano sem chamada externa
- **exporter.py** — Geração de pacote portátil
- **validator.py** — Validação de integridade e segurança
- **cli/__main__.py** — Interface de linha de comando

## Decisões de Design

- **Simplicidade antes de abstração:** Parser próprio de frontmatter, sem yaml externo
- **Determinístico:** Roteamento por scoring, não probabilístico
- **Local-first:** Tudo funciona sem API no modo base
- **Honestidade:** Adaptadores declaram requisitos, não fingem compatibilidade universal
- **Portabilidade:** Manifesto versionado, sem caminhos absolutos, sem segredos
