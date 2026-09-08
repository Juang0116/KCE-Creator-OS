from src.brand_brain.loader import BrandDNALoader
from src.brand_brain.relevance import RelevanceEngine
from src.radar.models import RadarSignal


def make_brand_dna():
    loader = BrandDNALoader(
        "schemas/brand_dna.schema.json"
    )

    return loader.load(
        "tests/fixtures/brand_dna_test.json"
    )


def make_signal(
    title,
    summary,
    keywords,
    topics,
):
    return RadarSignal(
        signal_id="signal_test",
        detected_at="2026-09-08T00:00:00+00:00",
        radar_version="0.1.0",
        source_type="rss",
        platform="rss",
        url="https://example.com/test",
        author="Test Author",
        published_at="2026-09-08T00:00:00+00:00",
        title=title,
        summary=summary,
        keywords=keywords,
        topics=topics,
        language="en",
        evidence={},
        niches=[],
        relevance_reason="",
        status="detected",
        confidence=0.8,
        processed_at=None,
    )


def test_brand_dna_loader_and_relevance_work_together():
    brand_dna = make_brand_dna()

    signal = make_signal(
        title="New AI tools for content creators",
        summary="Artificial intelligence is changing creator workflows.",
        keywords=["AI", "creators"],
        topics=["technology"],
    )

    engine = RelevanceEngine()

    result = engine.evaluate(
        signal,
        brand_dna,
    )

    assert result.score > 0
    assert result.level == "low"
    assert "technology" in result.matched_topics


def test_brand_dna_rejects_irrelevant_signal():
    brand_dna = make_brand_dna()

    signal = make_signal(
        title="New gardening techniques",
        summary="A guide to growing vegetables at home.",
        keywords=["gardening", "vegetables"],
        topics=["gardening"],
    )

    engine = RelevanceEngine()

    result = engine.evaluate(
        signal,
        brand_dna,
    )

    assert result.score < 0.50
    assert result.level == "low"


def test_brand_dna_relevance_matches_multiple_dimensions():
    brand_dna = make_brand_dna()

    signal = make_signal(
        title="AI technology for YouTube creators",
        summary="New technology helps creators produce better video content.",
        keywords=["AI", "creators", "technology"],
        topics=["technology", "AI"],
    )

    engine = RelevanceEngine()

    result = engine.evaluate(
        signal,
        brand_dna,
    )

    assert result.score > 0.50
    assert "ai" in result.matched_topics
    assert "technology" in result.matched_topics
    assert "ai" in result.matched_keywords