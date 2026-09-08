from src.brand_brain.relevance import RelevanceEngine
from src.radar.models import RadarSignal


def make_signal(
    keywords: list[str],
    topics: list[str],
) -> RadarSignal:
    return RadarSignal(
        signal_id="sig_test",
        detected_at="2026-09-08T00:00:00+00:00",
        radar_version="0.1.0",
        source_type="rss",
        platform="rss",
        url="https://example.com/article",
        author=None,
        published_at=None,
        title="Test signal",
        summary="Test summary",
        keywords=keywords,
        topics=topics,
        language="en",
        evidence={},
        niches=[],
        relevance_reason="",
        status="detected",
        confidence=0.5,
        processed_at=None,
    )


def test_relevance_detects_matching_brand_topics():
    signal = make_signal(
        keywords=[],
        topics=["technology"],
    )

    brand_dna = {
        "market": {
            "category": "technology",
        },
        "audience": {
            "interests": ["AI"],
            "problems": ["complex technology"],
            "desires": ["understand technology"],
        },
        "content": {
            "pillars": ["technology"],
            "topics": ["AI", "hardware"],
        },
    }

    result = RelevanceEngine().evaluate(
        signal,
        brand_dna,
    )

    assert result.matched_topics == ["technology"]
    assert result.score == 0.3
    assert result.level == "low"


def test_relevance_detects_keywords_and_topics():
    signal = make_signal(
        keywords=["AI", "chips"],
        topics=["technology", "hardware"],
    )

    brand_dna = {
        "market": {
            "category": "technology",
        },
        "audience": {
            "interests": ["AI", "chips"],
            "problems": ["complex technology"],
            "desires": ["understand technology"],
        },
        "content": {
            "pillars": ["technology"],
            "topics": ["hardware", "AI"],
        },
    }

    result = RelevanceEngine().evaluate(
        signal,
        brand_dna,
    )

    assert result.matched_keywords == ["ai", "chips"]
    assert result.matched_topics == [
        "hardware",
        "technology",
    ]
    assert result.score == 0.8667
    assert result.level == "high"


def test_relevance_returns_low_without_matches():
    signal = make_signal(
        keywords=["football"],
        topics=["sports"],
    )

    brand_dna = {
        "market": {
            "category": "technology",
        },
        "audience": {
            "interests": ["AI"],
            "problems": ["complex technology"],
            "desires": ["understand technology"],
        },
        "content": {
            "pillars": ["technology"],
            "topics": ["hardware"],
        },
    }

    result = RelevanceEngine().evaluate(
        signal,
        brand_dna,
    )

    assert result.score == 0.0
    assert result.level == "low"
    assert result.matched_keywords == []
    assert result.matched_topics == []
    assert result.reasons == [
        "No relevant Brand DNA matches found."
    ]