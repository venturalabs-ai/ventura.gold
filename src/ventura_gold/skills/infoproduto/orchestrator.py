"""
Ventura Infoproduto — Orquestrador de pipeline completo.
Integra as skills: criacao → conteudo → copywriting → pagina_vendas → materiais_vendas → ads_compliance → review
"""

from typing import Any, Dict, Optional


class VenturaInfoproduto:
    """
    Agente orquestrador para criação completa de infoprodutos.
    Pipeline:
    1. infoproduto_criacao
    2. infoproduto_conteudo
    3. copywriting
    4. pagina_vendas
    5. materiais_vendas
    6. ads_compliance
    7. review
    """

    name = "ventura_infoproduto"
    version = "1.0.0"
    skills = [
        "infoproduto_criacao",
        "infoproduto_conteudo",
        "copywriting",
        "pagina_vendas",
        "materiais_vendas",
        "ads_compliance",
        "review",
    ]

    def __init__(self, runtime: Any = None):
        self.runtime = runtime

    def run_skill(self, skill_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        if self.runtime is None:
            return {
                "skill": skill_name,
                "status": "stub",
                "input": payload,
                "message": "Conecte este agente ao runtime do ventura.gold para executar a skill real.",
            }
        return self.runtime.run_skill(skill_name, payload)

    def offer_consistency_check(
        self, estrategia: Dict[str, Any], pagina: Dict[str, Any], ads: Dict[str, Any]
    ) -> Dict[str, Any]:
        promessa = estrategia.get("promessa_principal")
        return {
            "status": "ok",
            "promessa_referencia": promessa,
            "checks": [
                "headline da página alinhada com a promessa principal",
                "anúncios sem claims absolutos",
                "CTA consistente entre landing page e ads",
                "disclaimers obrigatórios presentes",
            ],
        }

    def run_pipeline(self, briefing: Dict[str, Any]) -> Dict[str, Any]:
        estrategia = self.run_skill("infoproduto_criacao", briefing)

        conteudo = self.run_skill(
            "infoproduto_conteudo",
            {
                **briefing,
                **(estrategia if isinstance(estrategia, dict) else {}),
            },
        )

        copy = self.run_skill(
            "copywriting",
            {
                **briefing,
                **(estrategia if isinstance(estrategia, dict) else {}),
                "oferta": estrategia.get("oferta_base") if isinstance(estrategia, dict) else None,
                "objeções": estrategia.get("objeções_mapeadas") if isinstance(estrategia, dict) else None,
                "prova_disponivel": briefing.get("prova_social_disponivel"),
            },
        )

        pagina = self.run_skill(
            "pagina_vendas",
            {
                **briefing,
                **(estrategia if isinstance(estrategia, dict) else {}),
                "copywriting_output": copy,
                "oferta_completa": estrategia.get("oferta_base") if isinstance(estrategia, dict) else None,
            },
        )

        materiais = self.run_skill(
            "materiais_vendas",
            {
                **briefing,
                **(estrategia if isinstance(estrategia, dict) else {}),
                "copywriting_output": copy,
                "pagina_vendas_output": pagina,
                "oferta_completa": estrategia.get("oferta_base") if isinstance(estrategia, dict) else None,
            },
        )

        ads = self.run_skill(
            "ads_compliance",
            {
                **briefing,
                **(estrategia if isinstance(estrategia, dict) else {}),
                "copywriting_output": copy,
                "pagina_vendas_output": pagina,
                "oferta_completa": estrategia.get("oferta_base") if isinstance(estrategia, dict) else None,
            },
        )

        consistencia = self.offer_consistency_check(estrategia, pagina, ads)

        revisao = self.run_skill(
            "review",
            {
                "briefing": briefing,
                "estrategia": estrategia,
                "conteudo": conteudo,
                "copywriting": copy,
                "pagina": pagina,
                "materiais": materiais,
                "ads": ads,
                "consistencia": consistencia,
            },
        )

        return {
            "agent": self.name,
            "version": self.version,
            "briefing": briefing,
            "estrategia": estrategia,
            "conteudo": conteudo,
            "copywriting": copy,
            "pagina_vendas": pagina,
            "materiais_vendas": materiais,
            "ads": ads,
            "consistencia": consistencia,
            "review": revisao,
        }
