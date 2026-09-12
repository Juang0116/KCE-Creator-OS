import pytest

from src.brand_brain import BrandBrainV0
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


def make_signal(
    title="New AI technology changes the industry",
    keywords=None,
    topics=None,
):
    return RadarSignal(
        signal_id="sig_test_001",
        detected_at="2026-09-08T00:00:00+00:00",
        radar_version="0.1.0",
        source_type="rss",
        platform="rss",
        url="https://example.com/test",
        author="Test Source",
        published_at="2026-09-08T00:00:00+00:00",
        title=title,
        summary="A new development in AI and technology.",
        keywords=keywords or ["AI", "technology"],
        topics=topics or ["AI", "technology"],
        language="en",
        evidence={},
        niches=[],
        relevance_reason="",
        status="detected",
        confidence=0.8,
    )


def test_brand_brain_to_opportunity_engine():
    brand = make_brand()
    signal = make_signal()

    brain = BrandBrainV0()
    evaluation = brain.evaluate(signal, brand)

    engine = OpportunityEngineV0()
    opportunity = engine.evaluate(
        signal=signal,
        brand=brand,
        brand_evaluation=evaluation,
    )

    assert opportunity.signal_id == signal.signal_id
    assert opportunity.brand_id == brand["brand_id"]

    # Brand Brain uses a 0-100 relevance scale.
    # Opportunity Engine uses 0-10 for each scoring dimension.
    assert opportunity.scoring.relevance == pytest.approx(
        evaluation.relevance_score / 10
    )

    assert opportunity.processing.confidence == evaluation.confidence

    assert opportunity.analysis.recommendation in {
        "strong_candidate",
        "candidate",
        "weak_candidate",
        "reject",
    }

    assert 0 <= opportunity.scoring.total_score <= 100


def test_opportunity_uses_brand_brain_pillars():
    brand = make_brand()
    signal = make_signal()

    brain = BrandBrainV0()
    evaluation = brain.evaluate(signal, brand)

    engine = OpportunityEngineV0()
    opportunity = engine.evaluate(
        signal=signal,
        brand=brand,
        brand_evaluation=evaluation,
    )

    for pillar in evaluation.matched_pillars:
        assert pillar in opportunity.analysis.why_this_brand


def test_irrelevant_signal_does_not_become_strong_candidate():
    brand = make_brand()

    signal = make_signal(
        title="New football transfer announced",
        keywords=["football", "transfer"],
        topics=["football", "sports"],
    )

    brain = BrandBrainV0()
    evaluation = brain.evaluate(signal, brand)

    engine = OpportunityEngineV0()
    opportunity = engine.evaluate(
        signal=signal,
        brand=brand,
        brand_evaluation=evaluation,
    )

    assert evaluation.relevant is False

    # Same scale conversion: Brand Brain 0-100 → Opportunity 0-10.
    assert opportunity.scoring.relevance == pytest.approx(
        evaluation.relevance_score / 10
    )

    assert opportunity.scoring.total_score < 80