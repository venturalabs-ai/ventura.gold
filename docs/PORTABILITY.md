# Portabilidade e Formato

## Formato do pacote exportado

Arquivo `dist/ventura-agent-package.json`:

```json
{
  "format": "ventura-agent-package/v1",
  "name": "venture.gold",
  "version": "1.0.0",
  "authentication": "none-for-local-runtime",
  "portability": ["claude", "chatgpt", "..."],
  "agents": [],
  "skills": [],
  "adapters": []
}
```

## O que funciona em qualquer lugar

- Arquivos de instrução JSON — copiar e colar
- Roteamento baseado em regras — independente de modelo
- Estrutura de resposta — formato estável e previsível

## Diferenças entre plataformas

Cada adaptador declara honestamente:

- Se suporta instalação automática ou apenas cópia manual
- Se exige conta ou chave de API
- Limitações de tamanho, formato e persistência

O runtime local não tem login. Essa decisão vale para o software deste repositório; ela não pode e não deve burlar autenticação, políticas de uso, limites ou permissões das plataformas externas.
