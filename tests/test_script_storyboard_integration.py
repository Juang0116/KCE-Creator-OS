from src.content.ideas.models import (
    ContentAudience,
    ContentConcept,
    ContentIdea,
    ContentProcessing,
    ContentProduction,
    CreativeDirection,
)
from src.fact_check.models import (
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
from src.storyboard.engine import StoryboardEngineV0


def build_content_idea() -> ContentIdea:
    return ContentIdea(
        idea_id="idea_test_001",
        created_at="2026-09-08T18:00:00+00:00",
        idea_version="1",
        opportunity_id="opportunity_test_001",
        signal_id="signal_test_001",
        brand_id="futuro_tech",
        channel="Futuro Tech",
        platform="YouTube",
        concept=ContentConcept(
            working_title="La evolución de la inteligencia artificial",
            hook="La IA cambió mucho más rápido de lo que imaginábamos.",
            core_promise="Entender cómo evolucionó la inteligencia artificial.",
            angle="Explicar la evolución de forma sencilla.",
            format="long_form",
            estimated_duration_seconds=120,
            content_pillar="Artificial Intelligence",
        ),
        audience=ContentAudience(
            target="Personas interesadas en tecnología",
            audience_need="Entender la evolución de la IA.",
            expected_value="Una explicación clara y entretenida.",
        ),
        creative_direction=CreativeDirection(
            storytelling_approach="educational",
            visual_direction="Modern technology visuals",
            voice_direction="Clear and engaging",
            key_elements=["AI", "technology"],
        ),
        production=ContentProduction(
            complexity="medium",
            estimated_production_hours=3,
            required_assets=["technology visuals"],
            ai_assistance=["research", "visuals"],
        ),
        processing=ContentProcessing(
            status="draft",
            confidence=0.85,
            processed_at=None,
        ),
    )


def build_research() -> ResearchBrief:
    return ResearchBrief(
        research_id="research_test_001",
        created_at="2026-09-08T18:01:00+00:00",
        research_version="1",
        idea_id="idea_test_001",
        opportunity_id="opportunity_test_001",
        signal_id="signal_test_001",
        brand_id="futuro_tech",
        channel="Futuro Tech",
        platform="YouTube",
        objective=ResearchObjective(
            research_question="¿Cómo evolucionó la inteligencia artificial?",
            content_goal="Explicar la evolución de la IA.",
            key_questions=[
                "¿Cómo comenzó?",
                "¿Qué avances fueron importantes?",
            ],
        ),
        scope=ResearchScope(
            topics=["Artificial Intelligence"],
            keywords=["AI", "machine learning"],
            exclusions=[],
        ),
        findings=[],
        sources=[],
        research_gaps=[],
        processing=ResearchProcessing(
            status="draft",
            confidence=0.85,
            processed_at=None,
        ),
    )


def build_fact_check() -> FactCheck:
    checks = [
        FactCheckCheck(
            check_id="check_001",
            claim="La inteligencia artificial ha evolucionado durante décadas.",
            evidence="Test evidence 1",
            source_ids=["source_001"],
            verification_status="verified",
            confidence=0.95,
            notes="Verified for integration testing.",
        ),
        FactCheckCheck(
            check_id="check_002",
            claim="Los modelos modernos permiten nuevas formas de interacción.",
            evidence="Test evidence 2",
            source_ids=["source_002"],
            verification_status="partially_verified",
            confidence=0.80,
            notes="Partially verified for integration testing.",
        ),
    ]

    return FactCheck(
        fact_check_id="fact_check_test_001",
        created_at="2026-09-08T18:02:00+00:00",
        fact_check_version="1",
        research_id="research_test_001",
        idea_id="idea_test_001",
        opportunity_id="opportunity_test_001",
        signal_id="signal_test_001",
        brand_id="futuro_tech",
        channel="Futuro Tech",
        platform="YouTube",
        checks=checks,
        summary=FactCheckSummary(
            total_claims=2,
            verified_claims=1,
            partially_verified_claims=1,
            unverified_claims=0,
            refuted_claims=0,
            conflicting_claims=0,
        ),
        processing=FactCheckProcessing(
            status="draft",
            confidence=0.875,
            processed_at=None,
        ),
    )


def build_script():
    idea = build_content_idea()
    research = build_research()
    fact_check = build_fact_check()

    return ScriptEngineV0().generate(
        idea=idea,
        research=research,
        fact_check=fact_check,
    )


def test_script_sections_and_structure_become_storyboard_scenes():
    script = build_script()

    storyboard = StoryboardEngineV0().generate(script)

    assert storyboard.metadata.scene_count == len(storyboard.scenes)
    assert storyboard.metadata.scene_count == len(script.sections) + 4

    assert storyboard.scenes[0].section_id == "hook"
    assert storyboard.scenes[1].section_id == "introduction"
    assert storyboard.scenes[-2].section_id == "conclusion"
    assert storyboard.scenes[-1].section_id == "cta"

    section_scenes = storyboard.scenes[2:-2]

    assert len(section_scenes) == len(script.sections)

    for scene, section in zip(section_scenes, script.sections):
        assert scene.section_id == section.section_id
        assert scene.narration == section.narration
        assert scene.visual_direction == section.visual_direction
        assert scene.transition == section.transition


def test_storyboard_preserves_complete_script_lineage():
    script = build_script()

    storyboard = StoryboardEngineV0().generate(script)

    assert storyboard.source.script_id == script.script_id
    assert storyboard.source.idea_id == script.source.idea_id
    assert storyboard.source.research_id == script.source.research_id
    assert storyboard.source.fact_check_id == script.source.fact_check_id
    assert storyboard.source.opportunity_id == script.source.opportunity_id
    assert storyboard.source.signal_id == script.source.signal_id


def test_storyboard_preserves_target_metadata_and_confidence():
    script = build_script()

    storyboard = StoryboardEngineV0().generate(script)

    assert storyboard.target.brand_id == script.target.brand_id
    assert storyboard.target.channel == script.target.channel
    assert storyboard.target.platform == script.target.platform

    assert storyboard.metadata.title == script.metadata.title
    assert storyboard.metadata.format == script.metadata.format
    assert (
        storyboard.metadata.estimated_duration_seconds
        == script.metadata.estimated_duration_seconds
    )

    assert storyboard.processing.status == "draft"
    assert storyboard.processing.confidence == script.processing.confidence


def test_storyboard_contains_expected_v0_scene_defaults():
    script = build_script()

    storyboard = StoryboardEngineV0().generate(script)

    hook = storyboard.scenes[0]
    intro = storyboard.scenes[1]
    conclusion = storyboard.scenes[-2]
    cta = storyboard.scenes[-1]

    assert hook.shot_type == "opening"
    assert hook.visual_assets == ["intro_graphics"]

    assert intro.shot_type == "medium"
    assert intro.visual_assets == ["intro_graphics", "supporting_visuals"]

    assert conclusion.shot_type == "closing"
    assert conclusion.transition == "fade"

    assert cta.shot_type == "cta"
    assert cta.visual_assets == ["end_screen"]
