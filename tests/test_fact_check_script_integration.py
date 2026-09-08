from src.content.ideas.models import (
    ContentAudience,
    ContentConcept,
    ContentIdea,
    ContentProcessing,
    ContentProduction,
    CreativeDirection,
)
from src.fact_check import (
    FactCheck,
    FactCheckCheck,
    FactCheckProcessing,
    FactCheckSummary,
)
from src.research.models import (
    ResearchBrief,
    ResearchObjective,
    ResearchProcessing,
    ResearchScope,
)
from src.script.engine import ScriptEngineV0


def build_content_idea():
    return ContentIdea(
        idea_id="idea-001",
        created_at="2026-09-08T00:00:00Z",
        idea_version="1",
        opportunity_id="opportunity-001",
        signal_id="signal-001",
        brand_id="futuro-tech",
        channel="Futuro Tech",
        platform="YouTube",
        concept=ContentConcept(
            working_title="El futuro de la tecnología",
            hook="¿Estamos preparados para lo que viene?",
            core_promise=(
                "Entender cómo esta tecnología puede cambiar "
                "nuestras vidas."
            ),
            angle="Explicación clara y práctica",
            format="Explainer",
            estimated_duration_seconds=300,
            content_pillar="Tecnología",
        ),
        audience=ContentAudience(
            target="Personas interesadas en tecnología",
            audience_need="Entender nuevas tecnologías",
            expected_value="Una explicación clara y útil",
        ),
        creative_direction=CreativeDirection(
            storytelling_approach="Educativo y narrativo",
            visual_direction="Visuales tecnológicos modernos",
            voice_direction="Claro y educativo",
            key_elements=["Tecnología", "Explicación"],
        ),
        production=ContentProduction(
            complexity="medium",
            estimated_production_hours=3.0,
            required_assets=[],
            ai_assistance=["Investigación", "Visuales"],
        ),
        processing=ContentProcessing(
            status="draft",
            confidence=0.8,
        ),
    )


def build_research():
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
            research_question="¿Qué debemos verificar?",
            content_goal="Explicar el tema.",
            key_questions=["¿Cuál es el hecho principal?"],
        ),
        scope=ResearchScope(
            topics=["tecnología"],
            keywords=["tecnología"],
            exclusions=[],
        ),
        findings=[],
        sources=[],
        research_gaps=[],
        processing=ResearchProcessing(
            status="draft",
            confidence=0.8,
        ),
    )


def build_fact_check():
    checks = [
        FactCheckCheck(
            check_id="check-001",
            claim="La tecnología X fue presentada en 2024.",
            evidence="Evidencia de prueba.",
            source_ids=["source-001"],
            verification_status="verified",
            confidence=0.95,
        ),
        FactCheckCheck(
            check_id="check-002",
            claim="La tecnología X tiene más de un millón de usuarios.",
            evidence="Evidencia pendiente.",
            source_ids=["source-002"],
            verification_status="unverified",
            confidence=0.60,
        ),
    ]

    return FactCheck(
        fact_check_id="fact-check-001",
        created_at="2026-09-08T00:00:00Z",
        fact_check_version="1",
        research_id="research-001",
        idea_id="idea-001",
        opportunity_id="opportunity-001",
        signal_id="signal-001",
        brand_id="futuro-tech",
        channel="Futuro Tech",
        platform="YouTube",
        checks=checks,
        summary=FactCheckSummary(
            total_claims=2,
            verified_claims=1,
            partially_verified_claims=0,
            unverified_claims=1,
            refuted_claims=0,
            conflicting_claims=0,
        ),
        processing=FactCheckProcessing(
            status="draft",
            confidence=0.775,
        ),
    )


def test_fact_check_claims_become_script_claims():
    idea = build_content_idea()
    research = build_research()
    fact_check = build_fact_check()

    script = ScriptEngineV0().generate(
        idea,
        research,
        fact_check,
    )

    assert len(script.sections) == 2

    first_claim = script.sections[0].claims[0]
    second_claim = script.sections[1].claims[0]

    assert first_claim.claim == fact_check.checks[0].claim
    assert first_claim.fact_check_id == fact_check.fact_check_id
    assert first_claim.verification_status == "verified"

    assert second_claim.claim == fact_check.checks[1].claim
    assert second_claim.fact_check_id == fact_check.fact_check_id
    assert second_claim.verification_status == "unverified"


def test_script_preserves_fact_check_lineage():
    idea = build_content_idea()
    research = build_research()
    fact_check = build_fact_check()

    script = ScriptEngineV0().generate(
        idea,
        research,
        fact_check,
    )

    assert script.source.idea_id == idea.idea_id
    assert script.source.research_id == research.research_id
    assert script.source.fact_check_id == fact_check.fact_check_id
    assert script.source.opportunity_id == idea.opportunity_id
    assert script.source.signal_id == idea.signal_id


def test_script_preserves_content_target():
    idea = build_content_idea()
    research = build_research()
    fact_check = build_fact_check()

    script = ScriptEngineV0().generate(
        idea,
        research,
        fact_check,
    )

    assert script.target.brand_id == idea.brand_id
    assert script.target.channel == idea.channel
    assert script.target.platform == idea.platform