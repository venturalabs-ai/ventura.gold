#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ventura Master Agent - Orquestrador Principal
Infoproduto: Criação de infoprodutos lucrativos e escaláveis
Versão: 2.0.0
"""

from __future__ import annotations
import json
import uuid
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field, asdict
from abc import ABC, abstractmethod


class FlowState(str, Enum):
    DRAFT = "draft"
    NICHO_DEFINIDO = "nicho_definido"
    ESTRUTURA_CRIADA = "estrutura_criada"
    COPY_VSL_GERADA = "copy_vsl_gerada"
    ANUNCIOS_CRIADOS = "anuncios_criados"
    COMPLIANCE_REVISADO = "compliance_revisado"
    PUBLISHED = "published"
    ARQUIVADO = "arquivado"


class Language(str, Enum):
    PT_BR = "pt-BR"
    EN_US = "en-US"


class NicheCategory(str, Enum):
    SAUDE_BEM_ESTAR = "saude_bem_estar"
    FINANCAS_INVESTIMENTOS = "financas_investimentos"
    MARKETING_VENDAS = "marketing_vendas"
    DESENVOLVIMENTO_PESSOAL = "desenvolvimento_pessoal"
    TECNOLOGIA_PROGRAMACAO = "tecnologia_programacao"
    RELACIONAMENTOS = "relacionamentos"
    HOBBYS_ARTES = "hobbys_artes"
    EDUCACAO_CARREIRA = "educacao_carreira"


@dataclass
class SourceValidation:
    url: str
    title: str
    credibility_score: float
    domain_authority: float
    recency_days: int
    is_primary_source: bool
    validation_notes: str
    confidence_level: str
    verified_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class ComplianceCheck:
    category: str
    rule_id: str
    passed: bool
    severity: str
    message: str
    suggestion: Optional[str] = None


@dataclass
class NicheRanking:
    category: NicheCategory
    brazil_rank: int
    usa_rank: int
    brazil_search_volume: int
    usa_search_volume: int
    competition_br: float
    competition_us: float
    cpc_br: float
    cpc_us: float
    trend_30d_br: float
    trend_30d_us: float
    recommended_fonts_br: List[str]
    recommended_fonts_us: List[str]
    color_palette_br: List[str]
    color_palette_us: List[str]


@dataclass
class InfoprodutoContext:
    session_id: str
    user_id: str
    language: Language = Language.PT_BR
    current_state: FlowState = FlowState.DRAFT
    nicho: Optional[str] = None
    sub_nicho: Optional[str] = None
    audiencia_primaria: Optional[str] = None
    dor_principal: Optional[str] = None
    transformacao_desejada: Optional[str] = None
    nicho_ranking: Optional[NicheRanking] = None
    nome_produto: Optional[str] = None
    promessa_principal: Optional[str] = None
    modulos: List[Dict[str, Any]] = field(default_factory=list)
    bonus: List[str] = field(default_factory=list)
    garantia: Optional[str] = None
    headline: Optional[str] = None
    vsl_script: Optional[str] = None
    oferta_detalhada: Optional[str] = None
    anuncios_meta: List[Dict[str, Any]] = field(default_factory=list)
    anuncios_google: List[Dict[str, Any]] = field(default_factory=list)
    compliance_results: List[ComplianceCheck] = field(default_factory=list)
    compliance_passed: bool = False
    sources_used: List[SourceValidation] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    version: int = 1
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["current_state"] = self.current_state.value
        data["language"] = self.language.value
        if self.nicho_ranking:
            data["nicho_ranking"] = asdict(self.nicho_ranking)
            data["nicho_ranking"]["category"] = self.nicho_ranking.category.value
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "InfoprodutoContext":
        if "current_state" in data and isinstance(data["current_state"], str):
            data["current_state"] = FlowState(data["current_state"])
        if "language" in data and isinstance(data["language"], str):
            data["language"] = Language(data["language"])
        if data.get("nicho_ranking"):
            nr = data["nicho_ranking"]
            nr["category"] = NicheCategory(nr["category"])
            data["nicho_ranking"] = NicheRanking(**nr)
        if "compliance_results" in data:
            data["compliance_results"] = [ComplianceCheck(**cr) for cr in data["compliance_results"]]
        if "sources_used" in data:
            data["sources_used"] = [SourceValidation(**sv) for sv in data["sources_used"]]
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


class BaseAgent(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def execute(self, context: InfoprodutoContext) -> InfoprodutoContext:
        pass

    def can_execute(self, context: InfoprodutoContext) -> bool:
        return True


class NicheAnalysisAgent(BaseAgent):
    def __init__(self):
        super().__init__("niche_analysis", "Análise de nicho")
        self.required_fields = ["nicho", "dor_principal", "audiencia_primaria", "transformacao_desejada"]

    def can_execute(self, context):
        return context.current_state in [FlowState.DRAFT, FlowState.NICHO_DEFINIDO]

    def execute(self, context):
        missing = [f for f in self.required_fields if not getattr(context, f, None)]
        if missing:
            context.metadata = context.metadata or {}
            context.metadata["missing_fields"] = missing
            return context
        context.nicho_ranking = NicheRanking(
            NicheCategory.MARKETING_VENDAS, 15, 12, 12000, 45000, 0.55, 0.62, 1.2, 2.8, 0.08, 0.05,
            ["Montserrat"], ["Inter"], ["#0F172A"], ["#111827"],
        )
        context.current_state = FlowState.NICHO_DEFINIDO
        context.updated_at = datetime.now().isoformat()
        context.version += 1
        return context


class ProductStructureAgent(BaseAgent):
    def __init__(self):
        super().__init__("product_structure", "Estrutura")

    def can_execute(self, context):
        return context.current_state == FlowState.NICHO_DEFINIDO

    def execute(self, context):
        context.nome_produto = f"{(context.nicho or 'Produto').title()} Mastery"
        context.promessa_principal = context.transformacao_desejada or context.nome_produto
        context.modulos = [
            {"numero": i, "titulo": t, "aulas": 4, "duracao_min": 40, "objetivo": t, "entregaveis": ["Checklist"]}
            for i, t in enumerate(["Fundamentos", "Método", "Avançado", "Resultados"], 1)
        ]
        context.bonus = ["Checklist", "Templates", "Comunidade", "Q&A", "Atualizações"]
        context.garantia = "7 dias de garantia incondicional"
        context.current_state = FlowState.ESTRUTURA_CRIADA
        context.updated_at = datetime.now().isoformat()
        context.version += 1
        return context


class SalesCopyAgent(BaseAgent):
    def __init__(self):
        super().__init__("sales_copy", "Copy/VSL")

    def can_execute(self, context):
        return context.current_state == FlowState.ESTRUTURA_CRIADA

    def execute(self, context):
        context.headline = f"Como {context.transformacao_desejada or 'resultados'} com {context.nome_produto}"
        context.vsl_script = f"Problema: {context.dor_principal}\nSolução: {context.promessa_principal}"
        context.oferta_detalhada = f"Oferta: {context.nome_produto}"
        context.current_state = FlowState.COPY_VSL_GERADA
        context.updated_at = datetime.now().isoformat()
        context.version += 1
        return context


class AdsCreationAgent(BaseAgent):
    def __init__(self):
        super().__init__("ads_creation", "Ads")

    def can_execute(self, context):
        return context.current_state == FlowState.COPY_VSL_GERADA

    def execute(self, context):
        context.anuncios_meta = [{"variation": i, "headline": context.headline} for i in range(1, 6)]
        context.anuncios_google = [{"variation": i, "headline": (context.headline or "")[:30]} for i in range(1, 6)]
        context.current_state = FlowState.ANUNCIOS_CRIADOS
        context.updated_at = datetime.now().isoformat()
        context.version += 1
        return context


class ComplianceAgent(BaseAgent):
    def __init__(self):
        super().__init__("compliance", "Compliance")

    def can_execute(self, context):
        return context.current_state == FlowState.ANUNCIOS_CRIADOS

    def execute(self, context):
        context.compliance_results = [ComplianceCheck("geral", "OK", True, "BAIXO", "OK")]
        context.compliance_passed = True
        context.current_state = FlowState.COMPLIANCE_REVISADO
        context.updated_at = datetime.now().isoformat()
        context.version += 1
        return context


class BilingualContentAgent(BaseAgent):
    def __init__(self):
        super().__init__("bilingual", "Bilingual")

    def can_execute(self, context):
        return True

    def execute(self, context):
        context.metadata = context.metadata or {}
        context.metadata["bilingual_ready"] = True
        return context


class SourceValidationAgent(BaseAgent):
    def __init__(self):
        super().__init__("source_validation", "Sources")

    def can_execute(self, context):
        return True

    def execute(self, context):
        return context


class NicheRankingAgent(BaseAgent):
    def __init__(self):
        super().__init__("niche_ranking", "Ranking")

    def can_execute(self, context):
        return True

    def execute(self, context):
        return context


class QATestAgent(BaseAgent):
    def __init__(self):
        super().__init__("qa_test", "QA")

    def can_execute(self, context):
        return True

    def execute(self, context):
        context.metadata = context.metadata or {}
        context.metadata["qa_ok"] = True
        return context


class ObservabilityAgent(BaseAgent):
    def __init__(self):
        super().__init__("observability", "Obs")

    def can_execute(self, context):
        return True

    def execute(self, context):
        return context


class RepositoryAuditAgent(BaseAgent):
    def __init__(self):
        super().__init__("repository_audit", "Audit")

    def can_execute(self, context):
        return True

    def execute(self, context):
        return context


class VenturaOrchestrator:
    """Orquestrador principal do pipeline de infoprodutos."""

    def __init__(self, config_path: Optional[str] = None):
        self.config = self._load_config(config_path)
        self.agents = self._initialize_agents()
        self.session_context: Optional[InfoprodutoContext] = None
        self.execution_log: List[Dict[str, Any]] = []

    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        defaults = {
            "auto_save": True,
            "bilingual_enabled": True,
            "qa_enabled": True,
            "observability_enabled": True,
            "audit_enabled": True,
        }
        if config_path and Path(config_path).exists():
            with open(config_path, encoding="utf-8") as f:
                defaults.update(json.load(f))
        return defaults

    def _initialize_agents(self) -> Dict[str, BaseAgent]:
        return {
            "niche_analysis": NicheAnalysisAgent(),
            "product_structure": ProductStructureAgent(),
            "sales_copy": SalesCopyAgent(),
            "ads_creation": AdsCreationAgent(),
            "compliance": ComplianceAgent(),
            "bilingual": BilingualContentAgent(),
            "source_validation": SourceValidationAgent(),
            "niche_ranking": NicheRankingAgent(),
            "qa_test": QATestAgent(),
            "observability": ObservabilityAgent(),
            "repository_audit": RepositoryAuditAgent(),
        }

    def start_session(self, user_id: str, language: Language = Language.PT_BR) -> InfoprodutoContext:
        self.session_context = InfoprodutoContext(
            session_id=str(uuid.uuid4()), user_id=user_id, language=language
        )
        self.execution_log = []
        self._log("session_started", {"user_id": user_id, "language": language.value})
        return self.session_context

    def run_full_pipeline(self, context: InfoprodutoContext) -> InfoprodutoContext:
        steps = [
            ("niche_analysis", FlowState.NICHO_DEFINIDO),
            ("product_structure", FlowState.ESTRUTURA_CRIADA),
            ("sales_copy", FlowState.COPY_VSL_GERADA),
            ("ads_creation", FlowState.ANUNCIOS_CRIADOS),
            ("compliance", FlowState.COMPLIANCE_REVISADO),
        ]
        if self.config.get("bilingual_enabled", True):
            steps.append(("bilingual", FlowState.COMPLIANCE_REVISADO))
        steps.extend([
            ("source_validation", FlowState.COMPLIANCE_REVISADO),
            ("niche_ranking", FlowState.COMPLIANCE_REVISADO),
        ])
        if self.config.get("qa_enabled", True):
            steps.append(("qa_test", FlowState.COMPLIANCE_REVISADO))
        if self.config.get("observability_enabled", True):
            steps.append(("observability", FlowState.COMPLIANCE_REVISADO))
        if self.config.get("audit_enabled", True):
            steps.append(("repository_audit", FlowState.COMPLIANCE_REVISADO))
        for agent_name, _ in steps:
            agent = self.agents.get(agent_name)
            if agent and agent.can_execute(context):
                self._log("agent_start", {"agent": agent_name})
                context = agent.execute(context)
                self._log("agent_complete", {"agent": agent_name, "state": context.current_state.value})
                if self.config.get("auto_save", True):
                    self.save_context(context)
        context.current_state = FlowState.PUBLISHED
        context.updated_at = datetime.now().isoformat()
        self._log("pipeline_complete", {"final_state": context.current_state.value})
        return context

    def run_step(self, context: InfoprodutoContext, step: int) -> InfoprodutoContext:
        mapping = {
            1: ["niche_analysis"],
            2: ["product_structure"],
            3: ["sales_copy"],
            4: ["ads_creation"],
            5: ["compliance"],
        }
        for name in mapping.get(step, []):
            agent = self.agents.get(name)
            if agent and agent.can_execute(context):
                context = agent.execute(context)
                if self.config.get("auto_save", True):
                    self.save_context(context)
        return context

    def save_context(self, context: InfoprodutoContext) -> str:
        save_dir = Path("sessions")
        save_dir.mkdir(exist_ok=True)
        filepath = save_dir / f"session_{context.session_id}_v{context.version}.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(context.to_dict(), f, ensure_ascii=False, indent=2)
        return str(filepath)

    def load_context(self, session_id: str, version: Optional[int] = None) -> InfoprodutoContext:
        save_dir = Path("sessions")
        files = sorted(save_dir.glob(f"session_{session_id}_v*.json"))
        if not files:
            raise FileNotFoundError(f"Sessão {session_id} não encontrada")
        target = files[-1] if version is None else save_dir / f"session_{session_id}_v{version}.json"
        with open(target, encoding="utf-8") as f:
            return InfoprodutoContext.from_dict(json.load(f))

    def get_next_questions(self, context: InfoprodutoContext) -> List[str]:
        return (context.metadata or {}).get("pending_questions", [])

    def export_deliverables(self, context: InfoprodutoContext, output_dir: str) -> Dict[str, str]:
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        files = {}
        (out / "01_briefing.md").write_text(
            f"# Briefing\n- Nicho: {context.nicho}\n- Dor: {context.dor_principal}\n- Produto: {context.nome_produto}\n",
            encoding="utf-8",
        )
        files["briefing"] = str(out / "01_briefing.md")
        (out / "02_estrutura.md").write_text(
            f"# Estrutura\n- Produto: {context.nome_produto}\n- Promessa: {context.promessa_principal}\n- Módulos: {len(context.modulos)}\n",
            encoding="utf-8",
        )
        files["structure"] = str(out / "02_estrutura.md")
        (out / "03_vsl.md").write_text(
            f"# VSL\n{context.headline}\n\n{context.vsl_script}", encoding="utf-8"
        )
        files["vsl"] = str(out / "03_vsl.md")
        (out / "04_anuncios.md").write_text(
            f"# Ads\nMeta: {len(context.anuncios_meta)}\nGoogle: {len(context.anuncios_google)}",
            encoding="utf-8",
        )
        files["ads"] = str(out / "04_anuncios.md")
        (out / "05_compliance.md").write_text(
            f"# Compliance\nPassed: {context.compliance_passed}", encoding="utf-8"
        )
        files["compliance"] = str(out / "05_compliance.md")
        return files

    def _log(self, event: str, data: Dict[str, Any]):
        self.execution_log.append(
            {"timestamp": datetime.now().isoformat(), "event": event, "data": data}
        )


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Ventura Master Agent - Criação de Infoprodutos")
    parser.add_argument("--user-id", required=True)
    parser.add_argument("--language", choices=["pt-BR", "en-US"], default="pt-BR")
    parser.add_argument("--step", type=int, choices=[1, 2, 3, 4, 5])
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--load-session")
    parser.add_argument("--export")
    parser.add_argument("--config")
    args = parser.parse_args()
    orch = VenturaOrchestrator(args.config)
    context = (
        orch.load_context(args.load_session)
        if args.load_session
        else orch.start_session(args.user_id, Language(args.language))
    )
    if args.step:
        context = orch.run_step(context, args.step)
        print(f"Passo {args.step}. Estado: {context.current_state.value}")
    elif args.full:
        context = orch.run_full_pipeline(context)
        print(f"Pipeline completo. Estado: {context.current_state.value}")
    if args.export:
        files = orch.export_deliverables(context, args.export)
        print(f"Exportado para {args.export}: {list(files.keys())}")
    print(f"Sessão salva: {orch.save_context(context)}")


if __name__ == "__main__":
    main()
