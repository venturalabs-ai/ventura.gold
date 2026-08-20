# Automações do ventura.gold

Este documento descreve as automações disponíveis no repositório para transformar o
agente em um pipeline completo: **Skills**, **LLM**, **MCP** e **CI/CD**.

> Nota: este arquivo foi adicionado na consolidação pós-auditoria (ver `docs/AUDIT.md`).
> Ele descreve os comandos reais da CLI adotada (versão 1.1.0 — ecossistema Infoproduto).

## 1. CLI e fluxo principal (`ventura-gold`)

| Comando | Descrição |
|---------|-----------|
| `ventura-gold doctor` | Diagnóstico do ambiente (Python, agentes, skills, chaves) |
| `ventura-gold list` | Lista agentes, skills e adaptadores |
| `ventura-gold validate` | Valida estrutura, metadados e avisos de segurança |
| `ventura-gold export` | Exporta pacote portátil (`dist/ventura-agent-package.json`) |
| `ventura-gold run --prompt "..."` | Monta plano + instruções (LLM opcional via `--llm`) |
| `ventura-gold repo scan` | Estatísticas do repositório |
| `ventura-gold repo generate-code --spec` | Gera módulo a partir de especificação |
| `ventura-gold repo generate-tests --file` | Gera testes pytest a partir de um `.py` |
| `ventura-gold repo docs` | Gera documentação de repositório |
| `ventura-gold repo review` | Revisa o repositório |

## 2. Automação de Skills

- Skills organizadas em domínios aninhados em `src/ventura_gold/skills/`:
  `repository`, `codegen`, `testing`, `docs`, `review` e o ecossistema `infoproduto`.
- Formato por domínio: diretório com `SKILL.md` (frontmatter `id`, `name`,
  `description`, `capabilities`) e, quando aplicável, implementação em Python
  (`analyst.py`, `generator.py`, `builder.py`, `auditor.py`, `orchestrator.py`).
- Metadados JSON legados (`planning.json`, `research.json`, etc.) continuam
  descobertos pelo `registry` para compatibilidade.
- `ventura-gold validate` e o workflow de PR validam a estrutura dos metadados.

## 3. Automação LLM (opcional)

- `core/llm_client.py` — classe `LLMClient(provider, model)` com
  `generate_sync(prompt, system_prompt)`.
- `ventura-gold run --prompt "..." --llm claude` executa o plano montado contra um
  provedor configurado.
- **Local-first:** sem chave → modo local simulado (`providerResponse: null`), sem bloqueio.
- `.env.example` documenta as variáveis suportadas (nenhuma obrigatória).

## 4. Automação MCP (local)

- `mcp/server_git.py` — classe `GitServer` (status, diff, log, branch).
- `mcp/server_filesystem.py` — classe `FileSystemServer` com sandboxing de caminho
  (lista, leitura, escrita e busca restritas à raiz do repositório).
- Sem dependências externas; testável em processo (usado no workflow de PR).

## 5. Automação de repositório (`ventura-gold repo`)

- `scan` — arquivos, linhas, extensões e ativos do agente.
- `generate-code` / `generate-tests` — geração determinística (AST/templates),
  sem depender de LLM.
- `docs` / `review` — documentação e revisão assistida do repositório.

## 6. Automação CI/CD (GitHub Actions)

| Workflow | Disparo | Ações |
|----------|---------|-------|
| `ci.yml` | push `main` + PR | matriz Python 3.10–3.12, testes, doctor, scan, validate, export, scan de segredos |
| `pr-validation.yml` | PR | validação de estrutura/metadados + JSON + segredos + smoke test MCP |
| `package-export.yml` | push `main` | gera `dist/ventura-agent-package.json` como artefato |
| `release.yml` | tag `v*` | build sdist/wheel, release no GitHub e publicação no PyPI (trusted publishing) |

## Fluxo de uso recomendado

```bash
# Durante o desenvolvimento
ventura-gold repo scan
ventura-gold validate
ventura-gold repo generate-code --spec "módulo de cache LRU"
ventura-gold export

# Ao enviar código
git push   # CI + PR validation rodam automaticamente

# Ao publicar uma versão
git tag v1.2.0 && git push origin v1.2.0   # release.yml publica no PyPI
```
