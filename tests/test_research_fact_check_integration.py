from src.fact_check import FactCheckEngineV0
from src.research.models import (
    ResearchBrief,
    ResearchFinding,
    ResearchObjective,
    ResearchProcessing,
    ResearchScope,
)


def build_research_brief(findings=None):
    return ResearchBrief(
        research_id="research-001",
        created_at="2026-09-08T00:00:00Z",
        research_version="1",
        idea_id="idea-001",
        opportunity_id="opportunity-001",
        signal_id="signal-001",
        brand_id="futuro-tech",
        channel="Futuro Tech",
        platform="YouTube",
        objective=ResearchObjective(
            research_question=(
                "¿Qué necesitamos verificar para desarrollar "
                "el contenido?"
            ),
            content_goal="Explicar el tema de forma clara y útil.",
            key_questions=[
                "¿Cuál es el hecho principal?",
                "¿Qué evidencia existe?",
            ],
        ),
        scope=ResearchScope(
            topics=["tecnología"],
            keywords=["tecnología"],
            exclusions=[],
        ),
        findings=findings or [],
        sources=[],
        research_gaps=[],
        processing=ResearchProcessing(
            status="draft",
            confidence=0.8,
        ),
    )


def test_empty_research_generates_empty_fact_check():
    research = build_research_brief()

    fact_check = FactCheckEngineV0().generate(research)

    assert fact_check.research_id == research.research_id
    assert fact_check.checks == []
    assert fact_check.summary.total_claims == 0
    assert fact_check.processing.confidence == 0.0


def test_research_findings_become_unverified_checks():
    findings = [
        ResearchFinding(
            claim="La tecnología X fue lanzada en 2024.",
            evidence="Fuente pendiente de verificación.",
            source_id="source-001",
            confidence=0.75,
        ),
        ResearchFinding(
            claim="La tecnología X tiene más de un millón de usuarios.",
            evidence="Dato encontrado durante la investigación.",
            source_id="source-002",
            confidence=0.60,
        ),
    ]

    research = build_research_brief(findings)

    fact_check = FactCheckEngineV0().generate(research)

    assert len(fact_check.checks) == 2
    assert fact_check.summary.total_claims == 2
    assert fact_check.summary.unverified_claims == 2

    assert fact_check.checks[0].claim == findings[0].claim
    assert fact_check.checks[0].verification_status == "unverified"
    assert fact_check.checks[0].confidence == findings[0].confidence
    assert fact_check.checks[0].source_ids == ["source-001"]

    assert fact_check.checks[1].claim == findings[1].claim
    assert fact_check.checks[1].verification_status == "unverified"
    assert fact_check.checks[1].confidence == findings[1].confidence
    assert fact_check.checks[1].source_ids == ["source-002"]


def test_fact_check_preserves_research_lineage():
    research = build_research_brief()

    fact_check = FactCheckEngineV0().generate(research)

    assert fact_check.research_id == "research-001"
    assert fact_check.idea_id == "idea-001"
    assert fact_check.opportunity_id == "opportunity-001"
    assert fact_check.signal_id == "signal-001"
    assert fact_check.brand_id == "futuro-tech"
    assert fact_check.channel == "Futuro Tech"
    assert fact_check.platform == "YouTube"