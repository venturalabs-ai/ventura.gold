"""
Agente 2: Product Structure Agent
Criação da estrutura do infoproduto (módulos, promessa, bônus, garantia)
"""
from ..orchestrator import BaseAgent, InfoprodutoContext, FlowState, Language
from typing import List, Dict, Any
from datetime import datetime


class ProductStructureAgent(BaseAgent):
    """Agente especializado em estruturação de infoprodutos"""
    
    def __init__(self):
        super().__init__(
            "product_structure_agent",
            "Cria módulos, promessa, bônus, garantia e sugestão de precificação baseados no nicho e dor"
        )
    
    def can_execute(self, context: InfoprodutoContext) -> bool:
        return context.current_state == FlowState.NICHO_DEFINIDO
    
    def execute(self, context: InfoprodutoContext) -> InfoprodutoContext:
        context.nome_produto = self._generate_product_name(context)
        context.promessa_principal = self._generate_promise(context)
        context.modulos = self._generate_modules(context)
        context.bonus = self._generate_bonus(context)
        context.garantia = self._generate_guarantee(context)
        context.metadata = context.metadata or {}
        context.metadata['pricing_suggestion'] = self._suggest_pricing(context)
        
        context.current_state = FlowState.ESTRUTURA_CRIADA
        context.updated_at = datetime.now().isoformat()
        context.version += 1
        return context
    
    def _generate_product_name(self, context: InfoprodutoContext) -> str:
        nicho = (context.nicho or "Produto").title()
        templates = {
            Language.PT_BR: [f"{nicho} Mastery", f"Domine {nicho}", f"Método {nicho}"],
            Language.EN_US: [f"{nicho} Mastery", f"Master {nicho}", f"{nicho} Pro"],
        }
        return templates.get(context.language, templates[Language.PT_BR])[0]
    
    def _generate_promise(self, context: InfoprodutoContext) -> str:
        return f"{context.transformacao_desejada or 'Resultados práticos'} com o método {context.nome_produto or 'completo'}"
    
    def _generate_modules(self, context: InfoprodutoContext) -> List[Dict[str, Any]]:
        return [
            {"numero": 1, "titulo": "Fundamentos", "aulas": 4, "duracao_min": 40, "objetivo": "Base sólida", "entregaveis": ["Checklist"]},
            {"numero": 2, "titulo": "Método na prática", "aulas": 5, "duracao_min": 60, "objetivo": "Aplicação", "entregaveis": ["Template"]},
            {"numero": 3, "titulo": "Avançado", "aulas": 4, "duracao_min": 50, "objetivo": "Escala", "entregaveis": ["Planilha"]},
            {"numero": 4, "titulo": "Resultados e próximos passos", "aulas": 3, "duracao_min": 30, "objetivo": "Consolidação", "entregaveis": ["Roadmap"]},
        ]
    
    def _generate_bonus(self, context: InfoprodutoContext) -> List[str]:
        return [
            "Checklist de implementação rápida",
            "Templates prontos para usar",
            "Comunidade de suporte",
            "Sessão ao vivo de Q&A",
            "Atualizações vitalícias",
        ]
    
    def _generate_guarantee(self, context: InfoprodutoContext) -> str:
        return "Se em 7 dias você não ver valor, devolvemos 100% do investimento — sem perguntas."
    
    def _suggest_pricing(self, context: InfoprodutoContext) -> dict:
        return {"price_br": 497.0, "price_us": 97.0, "installments": 12}
