"""
Ventura Infoproduto — Orquestrador de pipeline completo.
Pipeline: criacao → conteudo → copywriting → pagina_vendas → materiais_vendas → ads_compliance → review
"""

from typing import Any, Dict


class VenturaInfoproduto:
    """
    Agente orquestrador para criação completa de infoprodutos.
    """

    name = "ventura_infoproduto"
    version = "1.1.0"
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

    def run_pipeline(self, briefing: Dict[str, Any]) -> Dict[str, Any]:
        # 1. Estratégia base
        estrategia = self.run_skill("infoproduto_criacao", briefing)

        # 2. Conteúdo do produto
        conteudo = self.run_skill("infoproduto_conteudo", {
            **briefing,
            **(estrategia if isinstance(estrategia, dict) else {}),
        })

        # 3. Copywriting (necessário para página e materiais)
        copy = self.run_skill("copywriting", {
            **briefing,
            **(estrategia if isinstance(estrategia, dict) else {}),
            "oferta": estrategia.get("oferta_base") if isinstance(estrategia, dict) else None,
            "objeções": estrategia.get("objeções_mapeadas") if isinstance(estrategia, dict) else None,
            "prova_disponivel": briefing.get("prova_social_disponivel"),
        })

        # 4. Página de vendas
        pagina = self.run_skill("pagina_vendas", {
            **briefing,
            **(estrategia if isinstance(estrategia, dict) else {}),
            "copywriting_output": copy,
            "oferta_completa": estrategia.get("oferta_base") if isinstance(estrategia, dict) else None,
        })

        # 5. Materiais de vendas (e-mail, WhatsApp, webinar, posts...)
        materiais = self.run_skill("materiais_vendas", {
            **briefing,
            **(estrategia if isinstance(estrategia, dict) else {}),
            "copywriting_output": copy,
            "pagina_vendas_output": pagina,
            "oferta_completa": estrategia.get("oferta_base") if isinstance(estrategia, dict) else None,
        })

        # 6. Anúncios + compliance
        ads = self.run_skill("ads_compliance", {
            **briefing,
            **(estrategia if isinstance(estrategia, dict) else {}),
            "copywriting_output": copy,
            "pagina_vendas_output": pagina,
            "oferta_completa": estrategia.get("oferta_base") if isinstance(estrategia, dict) else None,
        })

        # 7. Review final
        revisao = self.run_skill("review", {
            "briefing": briefing,
            "estrategia": estrategia,
            "conteudo": conteudo,
            "copywriting": copy,
            "pagina": pagina,
            "materiais": materiais,
            "ads": ads,
        })

        return {
            "agent": self.name,
            "version": self.version,
            "briefing": briefing,
            "estrategia": estrategia,
            "conteudo": conteudo,
            "copywriting": copy,
            "pagina": pagina,
            "materiais": materiais,
            "ads": ads,
            "revisao": revisao,
        }
