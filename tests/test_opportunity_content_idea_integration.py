from src.brand_brain import BrandBrainV0
from src.content.ideas import ContentIdeaEngineV0
from src.opportunity import OpportunityEngineV0
from src.radar import RadarSignal


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


def build_opportunity():
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

    return brand, signal, evaluation, opportunity


def test_opportunity_to_content_idea():
    brand, signal, evaluation, opportunity = build_opportunity()

    engine = ContentIdeaEngineV0()

    idea = engine.generate(
        opportunity=opportunity,
        brand=brand,
    )

    assert idea.opportunity_id == opportunity.opportunity_id
    assert idea.signal_id == signal.signal_id
    assert idea.brand_id == brand["brand_id"]

    assert idea.channel == opportunity.channel
    assert idea.platform == "youtube"

    assert idea.processing.status == "draft"
    assert 0 <= idea.processing.confidence <= 1


def test_content_idea_preserves_opportunity_context():
    brand, signal, evaluation, opportunity = build_opportunity()

    engine = ContentIdeaEngineV0()

    idea = engine.generate(
        opportunity=opportunity,
        brand=brand,
    )

    assert idea.concept.working_title == opportunity.analysis.why_now
    assert idea.concept.angle == opportunity.analysis.why_this_brand

    assert idea.concept.format == "explainer"
    assert idea.concept.estimated_duration_seconds == 600


def test_content_idea_uses_brand_audience_and_pillar():
    brand, signal, evaluation, opportunity = build_opportunity()

    engine = ContentIdeaEngineV0()

    idea = engine.generate(
        opportunity=opportunity,
        brand=brand,
    )

    assert idea.audience.target == brand["audience"]["target"]

    for interest in brand["audience"]["interests"][:3]:
        assert interest in idea.audience.audience_need

    assert idea.concept.content_pillar in brand["content"]["pillars"]