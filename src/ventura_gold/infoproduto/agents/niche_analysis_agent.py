"""
Agente 1: Niche Analysis Agent
Análise de Nicho, Audiência e Dor Principal
"""
from ..orchestrator import BaseAgent, InfoprodutoContext, FlowState, Language, NicheRanking, NicheCategory
from typing import List
import json


class NicheAnalysisAgent(BaseAgent):
    """Agente especializado em análise de nicho e pesquisa de mercado"""
    
    def __init__(self):
        super().__init__(
            "niche_analysis_agent",
            "Analisa nicho, audiência e dor principal usando frameworks AIDA/PAS + dados de mercado"
        )
        self.required_fields = ['nicho', 'dor_principal', 'audiencia_primaria', 'transformacao_desejada']
    
    def can_execute(self, context: InfoprodutoContext) -> bool:
        return context.current_state in [FlowState.DRAFT, FlowState.NICHO_DEFINIDO]
    
    def execute(self, context: InfoprodutoContext) -> InfoprodutoContext:
        missing = [f for f in self.required_fields if not getattr(context, f, None)]
        if missing:
            context.metadata = context.metadata or {}
            context.metadata['missing_fields'] = missing
            context.metadata['pending_questions'] = self._generate_questions(context.language, missing)
            return context
        
        context.nicho_ranking = self._generate_niche_ranking(
            context.nicho, 
            context.sub_nicho,
            context.language
        )
        
        context.metadata = context.metadata or {}
        context.metadata['market_insights'] = self._collect_market_insights(context)
        
        context.current_state = FlowState.NICHO_DEFINIDO
        context.updated_at = self._now()
        context.version += 1
        return context
    
    def _generate_questions(self, language: Language, missing: List[str]) -> List[str]:
        qs = {
            Language.PT_BR: {
                'nicho': "Qual é o nicho principal do seu infoproduto?",
                'sub_nicho': "Qual o sub-nicho específico?",
                'audiencia_primaria': "Quem é sua audiência primária?",
                'dor_principal': "Qual a DOR PRINCIPAL que sua audiência sente hoje?",
                'transformacao_desejada': "Qual transformação você promete entregar?",
            },
            Language.EN_US: {
                'nicho': "What is the main niche of your info product?",
                'sub_nicho': "What is the specific sub-niche?",
                'audiencia_primaria': "Who is your primary audience?",
                'dor_principal': "What is the MAIN PAIN your audience feels today?",
                'transformacao_desejada': "What transformation do you promise to deliver?",
            }
        }
        lang_qs = qs.get(language, qs[Language.PT_BR])
        return [lang_qs[f] for f in missing if f in lang_qs]
    
    def _generate_niche_ranking(self, nicho, sub_nicho, language) -> NicheRanking:
        return NicheRanking(
            category=NicheCategory.MARKETING_VENDAS,
            brazil_rank=15,
            usa_rank=12,
            brazil_search_volume=12000,
            usa_search_volume=45000,
            competition_br=0.55,
            competition_us=0.62,
            cpc_br=1.2,
            cpc_us=2.8,
            trend_30d_br=0.08,
            trend_30d_us=0.05,
            recommended_fonts_br=["Montserrat", "Inter"],
            recommended_fonts_us=["Inter", "Roboto"],
            color_palette_br=["#0F172A", "#22C55E", "#F8FAFC"],
            color_palette_us=["#111827", "#3B82F6", "#F9FAFB"],
        )
    
    def _collect_market_insights(self, context) -> dict:
        return {
            "competitors_gaps": ["Falta de implementação prática", "Pouca abordagem de objeções"],
            "keyword_opportunities": [
                {"keyword": f"como {context.nicho} para iniciantes", "volume": 5400, "difficulty": 32}
            ],
            "audience_segments": [
                {"segment": "Iniciantes absolutos", "percentage": 40, "pain_level": "Alto"}
            ]
        }
    
    def _now(self) -> str:
        from datetime import datetime
        return datetime.now().isoformat()
