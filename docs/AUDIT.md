# Auditoria do ventura.gold

Data: 2026-08-19
Alvo: `https://github.com/venturalabs-ai/ventura.gold` (branch `main`)

## Resumo executivo

O projeto tem uma base conceitual sólida (local-first, determinístico, extensível via JSON),
mas a árvore de código está **incompleta e inconsistentemente reestruturada**. O pacote
instalável atual não funciona: o comando `ventura-gold` falha com `ModuleNotFoundError` e
vários módulos prometidos na documentação não existem. Os 9 testes existentes passam apenas
porque importam pacotes "namespace" legados (`core.*`, sem `__init__.py`), mascarando o problema.

## Achados críticos (bloqueiam o uso)

1. **Entry point quebrado** — `pyproject.toml:36` define `ventura-gold = "ventura_gold.cli:app"`,
   porém `src/ventura_gold/cli.py` **não existe**. A CLI real vive em `src/cli/__main__.py`
   (script avulso que importa `core.*` e usa `argparse`, não Typer).

   ```text
   $ ventura-gold doctor
   Traceback (most recent call last): ...
   ModuleNotFoundError: No module named 'ventura_gold.cli'
   ```

2. **Import quebrado no pacote novo** — `src/ventura_gold/core/exporter.py:9` importa
   `from .registry import ...`, mas `ventura_gold/core/registry.py` **não existe**.

3. **Módulos prometidos e ausentes** — README e mensagens de commit anunciam, mas não entregam:
   - `src/ventura_gold/core/{registry,router,runtime,frontmatter,llm_client}.py`
   - `src/ventura_gold/mcp/` (servidores de ferramentas Git + filesystem)
   - CLI `repo scan`, `repo generate-code`, `repo generate-tests`
   - O commit `a92a24c` diz "add ventura_gold core modules (context, exporter, router, registry, runtime, validator)" mas só adicionou `context`, `exporter`, `validator`.

4. **`ventura_gold/core/validator.py` referencia caminhos inexistentes**
   (`src/ventura_gold/core/router.py`, `runtime.py`, `cli.py`).

## Achados estruturais

5. **Duas árvores paralelas e divergentes:**
   - Legado (não empacotado): `src/core/`, `src/adapters/`, `src/cli/`, `src/skills/`, `src/agents/` — sem `__init__.py`, funcionam só via namespace package com `PYTHONPATH=src`.
   - Nova (empacotada, incompleta): `src/ventura_gold/`.
   - Os adaptadores das duas árvores divergem (a legada tem campo `steps`, a nova não).
   - Os testes importam a árvore legada (`from core.router import ...`).

6. **Stubs mortos** — `src/venture/__init__.py` e `src/venture/gold/__init__.py` são vazios
   e não são usados por ninguém.

7. **CI inconsistentemente referenciada** — `.github/workflows/ci.yml` executa
   `ventura-gold doctor`, `ventura-gold repo scan`, `ventura-gold validate`, `ventura-gold export`;
   como a CLI está quebrada e `repo scan` não existe, **a CI está vermelha**.

## Qualidade de código

8. Avisos via `print()` em vez de `logging` (`src/core/registry.py`).
9. Caminhos de descoberta acoplados à localização física do arquivo
   (`_CORE_DIR.parent / "agents"`), o que quebra em pacote instalado — mitigado com injeção de raiz.
10. `router.py` mistura mensagens de roteamento em português com código em inglês; aceitável,
    mas deve ser documentado como contrato público.
11. Falta `mcp/` na lista de pacotes do `pyproject.toml`; `[tool.setuptools.package-data]` promete
    `agents/*.json` e `skills/*.json` dentro de `ventura_gold`, mas `ventura_gold/skills/` não existe.

## Segurança (positivo)

- Sem segredos hardcoded; `.env` no `.gitignore`; `.env.example` com placeholders.
- Verificação de padrões de segredo na CI (regex de `sk-ant-`, `sk-proj-`, `ghp_`, `xai-`).
- Limite de 100k caracteres de prompt no runtime.
- Sem execução de shell a partir de prompt.

## Recomendações (implementadas nesta automação)

1. Consolidar tudo dentro de `ventura_gold` e tornar o pacote instalável e funcional.
2. Implementar `llm_client.py` (LLM opcional por env vars padrão de cada provedor).
3. Implementar `ventura_gold/mcp/` (tools + servidor JSON-RPC stdio).
4. Implementar CLI Typer com `doctor`, `list`, `validate`, `export`, `run`, `repo`,
   `skill`, `llm`, `mcp`.
5. Empacotar skills JSON dentro do pacote.
6. Corrigir testes para importar `ventura_gold.*` e adicionar cobertura nova.
7. Corrigir a CI e adicionar workflows de validação de PR, release e export de artefato.
8. Remover a árvore legada (`src/core/`, `src/adapters/`, `src/cli/`, `src/skills/`,
   `src/agents/`, `src/venture/`) — **concluído** em 2026-08-19 após confirmação do mantenedor.
   A descoberta agora usa apenas dados empacotados de `ventura_gold` (ou diretórios
   `src/agents`/`src/skills` do projeto quando presentes).

## Status pós-integração (2026-08-19)

Durante esta auditoria, o repositório remoto evoluiu em paralelo para **v1.1.0**
(ecossistema Infoproduto v2): agentes em `.md`, skills por domínio aninhadas
(`repository`, `codegen`, `testing`, `docs`, `review`, `infoproduto`), `llm_client.py`,
servidores MCP (`server_git.py`, `server_filesystem.py`) e CLI Typer com
`repo scan/generate-code/generate-tests/docs/review`.

Integração adotada (branch `main`):

- **Base**: estado remoto v1.1.0 (trabalho autoritativo preservado, sem force push).
- **Adições desta auditoria**: `docs/AUDIT.md`, `docs/AUTOMATION.md` e os workflows
  `.github/workflows/pr-validation.yml`, `package-export.yml` e `release.yml`.
- A maioria das recomendações acima já estava coberta pela evolução v2; a contribuição
  final é a validação automatizada adicional (PR, export de artefato e release) e a
  documentação de automações.
