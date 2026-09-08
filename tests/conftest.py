import pytest

from src.content.ideas.models import (
    ContentIdea,
    ContentConcept,
    ContentAudience,
    CreativeDirection,
    ContentProduction,
    ContentProcessing,
)

from src.research.models import (
    ResearchBrief,
    ResearchObjective,
    ResearchScope,
    ResearchProcessing,
)

from src.fact_check.models import (
    FactCheck,
    FactCheckCheck,
    FactCheckSummary,
    FactCheckProcessing,
)


@pytest.fixture
def sample_content_idea():
    return ContentIdea(
        idea_id="idea_test_001",
        created_at="2026-09-07T00:00:00+00:00",
        idea_version="1.0",
        opportunity_id="opp_test_001",
        signal_id="sig_test_001",
        brand_id="futuro_tech",
        channel="Futuro Tech",
        platform="YouTube",
        concept=ContentConcept(
            working_title="¿Qué está cambiando en la tecnología?",
            hook="La tecnología está cambiando más rápido de lo que creemos.",
            core_promise="Explicar los principales cambios tecnológicos.",
            angle="Educativo y accesible",
            format="Long-form video",
            estimated_duration_seconds=600,
            content_pillar="Technology",
        ),
        audience=ContentAudience(
            target="Personas interesadas en tecnología",
            audience_need="Entender tendencias tecnológicas",
            expected_value="Obtener contexto claro y útil",
        ),
        creative_direction=CreativeDirection(
            storytelling_approach="Explicación progresiva",
            visual_direction="Gráficos, capturas y ejemplos visuales",
            voice_direction="Claro, profesional y cercano",
            key_elements=["tecnología", "IA", "innovación"],
        ),
        production=ContentProduction(
            complexity="medium",
            estimated_production_hours=3.0,
            required_assets=["gráficos", "capturas"],
            ai_assistance=True,
        ),
        processing=ContentProcessing(
            status="draft",
            confidence=0.9,
            processed_at=None,
        ),
    )


@pytest.fixture
def sample_research_brief():
    return ResearchBrief(
        research_id="research_test_001",
        created_at="2026-09-07T00:00:00+00:00",
        research_version="1.0",
        idea_id="idea_test_001",
        opportunity_id="opp_test_001",
        signal_id="sig_test_001",
        brand_id="futuro_tech",
        channel="Futuro Tech",
        platform="YouTube",
        objective=ResearchObjective(
            research_question="¿Qué cambios tecnológicos son relevantes?",
            content_goal="Crear contenido educativo sobre tecnología.",
            key_questions=[
                "¿Qué tendencias son relevantes?",
                "¿Por qué importan?",
            ],
        ),
        scope=ResearchScope(
            topics=["Technology", "AI"],
            keywords=["technology", "AI", "innovation"],
            exclusions=[],
        ),
        findings=[],
        sources=[],
        research_gaps=[],
        processing=ResearchProcessing(
            status="draft",
            confidence=0.9,
            processed_at=None,
        ),
    )


@pytest.fixture
def sample_fact_check():
    checks = [
        FactCheckCheck(
            check_id="check_test_001",
            claim="La inteligencia artificial está transformando múltiples industrias.",
            evidence="Test evidence",
            source_ids=[],
            verification_status="unverified",
            confidence=0.5,
            notes="Test claim.",
        ),
        FactCheckCheck(
            check_id="check_test_002",
            claim="La automatización está cambiando determinados procesos de trabajo.",
            evidence="Test evidence",
            source_ids=[],
            verification_status="partially_verified",
            confidence=0.7,
            notes="Test claim.",
        ),
    ]

    return FactCheck(
        fact_check_id="fact_test_001",
        created_at="2026-09-07T00:00:00+00:00",
        fact_check_version="1.0",
        research_id="research_test_001",
        idea_id="idea_test_001",
        opportunity_id="opp_test_001",
        signal_id="sig_test_001",
        brand_id="futuro_tech",
        channel="Futuro Tech",
        platform="YouTube",
        checks=checks,
        summary=FactCheckSummary(
            total_claims=2,
            verified_claims=0,
            partially_verified_claims=1,
            unverified_claims=1,
            refuted_claims=0,
            conflicting_claims=0,
        ),
        processing=FactCheckProcessing(
            status="draft",
            confidence=0.6,
            processed_at=None,
        ),
    )

    return FactCheck(
        schema_version="1.0",
        fact_check_id="fact_test_001",
        created_at="2026-09-07T00:00:00+00:00",
        fact_check_version=1,
        source={
            "research_id": "research_test_001",
            "idea_id": "idea_test_001",
            "opportunity_id": "opp_test_001",
            "signal_id": "sig_test_001",
        },
        target={
            "brand_id": "futuro_tech",
            "channel": "Futuro Tech",
            "platform": "YouTube",
        },
        checks=checks,
        summary=FactCheckSummary(
            total_claims=2,
            verified_claims=0,
            partially_verified_claims=1,
            unverified_claims=1,
            refuted_claims=0,
            conflicting_claims=0,
        ),
        processing=FactCheckProcessing(
            status="draft",
            confidence=0.6,
            processed_at=None,
        ),
    )