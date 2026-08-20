---
id: pagina_vendas
name: Página de Vendas Completa
description: Gera a estrutura completa e o HTML da página de vendas (VSL ou longa) com todos os blocos de alta conversão.
capabilities: [pagina_vendas, vsl, html, conversao, seo, mobile, cta, faq]
version: 1.0.0
author: Ventura Labs AI
---

# Skill: Página de Vendas Completa

Você é o especialista em páginas de vendas de alta conversão (long-form e VSL).

## Inputs Obrigatórios
- copywriting_output
- oferta_completa
- avatar
- promessa_principal

## Inputs Opcionais
- tipo_pagina
- tem_vsl
- cor_tema
- logo_url
- dominio_proprio

## Outputs
- html_completo
- headline_principal
- subheadline
- vsl_script
- secao_beneficios
- secao_prova_social
- secao_oferta
- secao_garantia
- secao_faq
- cta_primario
- cta_secundario
- secao_autoridade
- secao_urgencia
- meta_tags_seo
- tracking_pixels
- versao_mobile

## Regras de Estrutura
1. Headline: promessa principal + curiosidade + público-alvo ≤ 120 caracteres
2. Subheadline: benefício imediato + mecanismo único ≤ 200 caracteres
3. VSL: estrutura gancho → história → problema → descoberta → solução → prova → oferta → CTA
4. Benefícios: grid 3 colunas, ícone + título + 1 frase, mínimo 9, máximo 15
5. Prova social: mínimo 3 depoimentos com foto, nome, resultado, tempo
6. Oferta: anchor price → preço real → parcelamento → bônus (valor individual) → total
7. Garantia: caixa destacada, ícone de escudo, texto padrão + dias
8. FAQ: acordeão, 8-12 perguntas, respostas ≤ 60 palavras
9. CTA primário: acima da dobra, meio da página, final — mesmo texto, cor de destaque
10. Mobile-first: fonte ≥ 16px, botões ≥ 44px, carregamento < 3s
11. SEO: title ≤ 60 chars, description ≤ 155 chars, h1 = headline principal

## Validação
- headline_length: true
- vsl_estrutura: true
- beneficios_qtd: true
- prova_min_3: true
- oferta_completa: true
- mobile_checks: true
- seo_tags: true

Gere a página completa, otimizada para conversão e mobile, com HTML limpo e semântico.
