from src.brand_brain import BrandBrainV0
from src.content.ideas import ContentIdeaEngineV0
from src.opportunity import OpportunityEngineV0
from src.radar import RadarSignal
from src.research import ResearchEngineV0


def make_brand():
    return {
        "brand_id": "brand_futuro_tech",
        "identity": {
            "name": "Futuro Tech",
        },
        "market": {
            "category": "technology",
            "competitors": [],
            "differentiators": [
                "educational technology content",
            ],
        },
        "audience": {
            "target": "people interested in technology",
            "age": "18-40",
            "interests": [
                "technology",
                "AI",
            ],
            "problems": [
                "understanding new technology",
            ],
            "desires": [
                "learning technology",
            ],
        },
        "personality": {
            "archetype": "Sage",
            "tone": "clear",
            "voice": "educational",
            "attitude": "curious",
        },
        "content": {
            "pillars": [
                "technology",
                "AI",
            ],
            "formats": [
                "educational",
            ],
            "topics": [
                "technology",
                "AI",
            ],
            "storytelling": [
                "explain",
            ],
        },
        "channels_community": {
            "primary_platforms": [
                "youtube",
            ],
        },
    }


def make_signal():
    return RadarSignal(
        signal_id="sig_test_001",
        detected_at="2026-09-08T00:00:00+00:00",
        radar_version="0.1.0",
        source_type="rss",
        platform="rss",
        url="https://example.com/test",
        author="Test Source",
        published_at="2026-09-08T00:00:00+00:00",
        title="New AI technology changes the industry",
        summary="A new development in AI and technology.",
        keywords=["AI", "technology"],
        topics=["AI", "technology"],
        language="en",
        evidence={},
        niches=[],
        relevance_reason="",
        status="detected",
        confidence=0.8,
    )


def build_content_idea():
    brand = make_brand()
    signal = make_signal()

    brain = BrandBrainV0()
    evaluation = brain.evaluate(signal, brand)

    opportunity_engine = OpportunityEngineV0()

    opportunity = opportunity_engine.evaluate(
        signal=signal,
        brand=brand,
        brand_evaluation=evaluation,
    )

    idea_engine = ContentIdeaEngineV0()

    idea = idea_engine.generate(
        opportunity=opportunity,
        brand=brand,
    )

    return brand, signal, opportunity, idea


def test_content_idea_to_research_brief():
    brand, signal, opportunity, idea = build_content_idea()

    engine = ResearchEngineV0()

    research = engine.generate(
        content_idea=idea,
        brand=brand,
    )

    assert research.idea_id == idea.idea_id
    assert research.opportunity_id == opportunity.opportunity_id
    assert research.signal_id == signal.signal_id
    assert research.brand_id == brand["brand_id"]

    assert research.channel == idea.channel
    assert research.platform == idea.platform

    assert research.processing.status == "draft"
    assert 0 <= research.processing.confidence <= 1


def test_research_preserves_content_idea_context():
    brand, signal, opportunity, idea = build_content_idea()

    engine = ResearchEngineV0()

    research = engine.generate(
        content_idea=idea,
        brand=brand,
    )

    assert idea.concept.working_title in (
        research.objective.research_question
    )

    assert (
        research.objective.content_goal
        == idea.concept.core_promise
    )

    assert len(research.objective.key_questions) == 4


def test_research_scope_uses_brand_content():
    brand, signal, opportunity, idea = build_content_idea()

    engine = ResearchEngineV0()

    research = engine.generate(
        content_idea=idea,
        brand=brand,
    )

    assert (
        idea.concept.content_pillar
        in research.scope.topics
    )

    for topic in brand["content"]["topics"]:
        assert topic in research.scope.topics
        assert topic in research.scope.keywords

    assert (
        "Información no relacionada con el objetivo del contenido."
        in research.scope.exclusions
    )

    assert (
        "Afirmaciones sin fuente verificable."
        in research.scope.exclusions
    )


def test_research_starts_without_unverified_findings():
    brand, signal, opportunity, idea = build_content_idea()

    engine = ResearchEngineV0()

    research = engine.generate(
        content_idea=idea,
        brand=brand,
    )

    assert research.findings == []
    assert research.sources == []
    assert research.research_gaps == []
    