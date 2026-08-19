# Instalação e Configuração

## Requisitos

- Python 3.10 ou superior
- pip (incluído na instalação do Python)

## Passo a passo

```bash
# 1. Obter o código
git clone https://github.com/venturalabs-ai/ventura.gold.git
cd venture.gold

# 2. Instalar dependências (nenhuma dependência de runtime externa)
pip install -e .

# 3. Verificar instalação
ventura-gold doctor

# ✅ Pronto para uso local — sem chave, sem cadastro
```

## Integrações opcionais (API)

Renomeie `.env.example` para `.env` e preencha as chaves que deseja usar.  
**Nenhuma é obrigatória.** O arquivo `.env` nunca deve ser enviado ao repositório.

## Publicação segura

- Nunca faça commit de `.env`, tokens ou chaves.
- Use `ventura-gold validate` antes de qualquer push.
- A CI verifica ausência de segredos óbvios.
