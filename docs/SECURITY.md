# Segurança e Modelo de Ameaça

## Práticas adotadas

- Nenhum segredo hardcoded no código
- `.env` no `.gitignore` — nunca enviado ao repositório
- Valores de exemplo em `.env.example`
- Nenhuma coleta silenciosa de dados
- Nenhuma execução de shell a partir de prompt
- Limite de tamanho de entrada (100k caracteres)
- Validação de integridade antes de exportar
- CI com verificação de padrões de segredos

## Política de avisos

> Aviso de segurança = recomendação, **não** bloqueio de uso

O sistema aponta riscos e boas práticas mas **nunca recusa** a solicitação apenas por isso.

## O que NÃO fazemos

- Não coletamos telemetria
- Não enviamos prompts a terceiros sem sua ação explícita
- Não persistimos credenciais em arquivos versionáveis
- Não burlamos autenticação de plataformas externas
- Não avaliamos código arbitrário sem consentimento explícito
