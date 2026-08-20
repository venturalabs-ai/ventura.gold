"""
Ventura Infoproduto — Ecossistema completo de criação de infoprodutos.

Pipeline com state machine:
  DRAFT → NICHO_DEFINIDO → ESTRUTURA_CRIADA → COPY_VSL_GERADA
       → ANUNCIOS_CRIADOS → COMPLIANCE_REVISADO → PUBLISHED
"""

from .orchestrator import (
    VenturaOrchestrator,
    InfoprodutoContext,
    FlowState,
    Language,
    NicheCategory,
    SourceValidation,
    ComplianceCheck,
    NicheRanking,
    BaseAgent,
)

__all__ = [
    "VenturaOrchestrator",
    "InfoprodutoContext",
    "FlowState",
    "Language",
    "NicheCategory",
    "SourceValidation",
    "ComplianceCheck",
    "NicheRanking",
    "BaseAgent",
]

__version__ = "2.0.0"
