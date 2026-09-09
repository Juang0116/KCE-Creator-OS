from src.brand_brain import BrandBrainV0
from src.content.ideas import ContentIdeaEngineV0
from src.discovery import (
    DiscoveryEngineV0,
    DiscoveryProcessing,
    DiscoveryResult,
)
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
        signal_id="sig_discovery_001",
        detected_at="2026-09-09T00:00:00+00:00",
        radar_version="0.1.0",
        source_type="rss",
        platform="rss",
        url="https://example.com/discovery",
        author="Test Source",
        published_at="2026-09-09T00:00:00+00:00",
        title="New AI technology changes the industry",
        summary="A new development in AI and technology.",
        keywords=[
            "AI",
            "technology",
        ],
        topics=[
            "AI",
            "technology",
        ],
        language="en",
        evidence={},
        niches=[],
        relevance_reason="",
        status="detected",
        confidence=0.8,
    )


def make_irrelevant_signal():
    return RadarSignal(
        signal_id="sig_discovery_irrelevant",
        detected_at="2026-09-09T00:00:00+00:00",
        radar_version="0.1.0",
        source_type="rss",
        platform="rss",
        url="https://example.com/irrelevant",
        author="Test Source",
        published_at="2026-09-09T00:00:00+00:00",
        title="New gardening technique becomes popular",
        summary="A gardening technique is attracting attention.",
        keywords=[
            "gardening",
            "plants",
            "flowers",
        ],
        topics=[
            "gardening",
            "plants",
        ],
        language="en",
        evidence={},
        niches=[],
        relevance_reason="",
        status="detected",
        confidence=0.8,
    )


def build_pipeline():
    brand = make_brand()
    signal = make_signal()

    brand_brain = BrandBrainV0()

    brand_evaluation = brand_brain.evaluate(
        signal,
        brand,
    )

    opportunity_engine = OpportunityEngineV0()

    opportunity = opportunity_engine.evaluate(
        signal=signal,
        brand=brand,
        brand_evaluation=brand_evaluation,
    )

    idea_engine = ContentIdeaEngineV0()

    idea = idea_engine.generate(
        opportunity=opportunity,
        brand=brand,
    )

    return (
        brand,
        signal,
        brand_evaluation,
        opportunity,
        idea,
    )


def test_discovery_processing_defaults():
    processing = DiscoveryProcessing()

    assert processing.status == "draft"
    assert processing.confidence == 0.0
    assert processing.processed_at is None


def test_discovery_processing_serialization():
    processing = DiscoveryProcessing(
        status="approved",
        confidence=0.95,
        processed_at="2026-09-09T12:00:00+00:00",
    )

    data = processing.to_dict()

    assert data == {
        "status": "approved",
        "confidence": 0.95,
        "processed_at": "2026-09-09T12:00:00+00:00",
    }


def test_discovery_result_preserves_lineage():
    (
        brand,
        signal,
        brand_evaluation,
        opportunity,
        idea,
    ) = build_pipeline()

    discovery = DiscoveryResult(
        discovery_id="discovery_001",
        created_at="2026-09-09T12:00:00+00:00",
        discovery_version="0.1.0",
        signal=signal,
        brand_evaluation=brand_evaluation,
        opportunity=opportunity,
        idea=idea,
    )

    assert discovery.signal.signal_id == signal.signal_id

    assert (
        discovery.brand_evaluation.signal_id
        == signal.signal_id
    )

    assert (
        discovery.opportunity.signal_id
        == signal.signal_id
    )

    assert (
        discovery.opportunity.brand_id
        == brand["brand_id"]
    )

    assert (
        idea.opportunity_id
        == opportunity.opportunity_id
    )

    assert idea.signal_id == signal.signal_id


def test_discovery_result_serialization():
    (
        _brand,
        signal,
        brand_evaluation,
        opportunity,
        idea,
    ) = build_pipeline()

    discovery = DiscoveryResult(
        discovery_id="discovery_002",
        created_at="2026-09-09T12:00:00+00:00",
        discovery_version="0.1.0",
        signal=signal,
        brand_evaluation=brand_evaluation,
        opportunity=opportunity,
        idea=idea,
    )

    data = discovery.to_dict()

    assert data["schema_version"] == "1.0.0"
    assert data["discovery_id"] == "discovery_002"
    assert data["discovery_version"] == "0.1.0"

    assert (
        data["signal"]["signal_id"]
        == signal.signal_id
    )

    assert (
        data["brand_evaluation"]["signal_id"]
        == signal.signal_id
    )

    assert (
        data["opportunity"]["opportunity_id"]
        == opportunity.opportunity_id
    )

    assert (
        data["idea"]["idea_id"]
        == idea.idea_id
    )

    assert data["processing"]["status"] == "draft"


def test_discovery_engine_runs_full_circuit():
    brand = make_brand()
    signal = make_signal()

    result = DiscoveryEngineV0().run(
        signal=signal,
        brand=brand,
    )

    assert isinstance(result, DiscoveryResult)

    assert result.signal.signal_id == signal.signal_id

    assert (
        result.brand_evaluation.signal_id
        == signal.signal_id
    )

    assert (
        result.brand_evaluation.brand_id
        == brand["brand_id"]
    )

    assert (
        result.opportunity.signal_id
        == signal.signal_id
    )

    assert (
        result.opportunity.brand_id
        == brand["brand_id"]
    )

    assert (
        result.idea.opportunity_id
        == result.opportunity.opportunity_id
    )

    assert (
        result.idea.signal_id
        == signal.signal_id
    )

    assert (
        result.idea.brand_id
        == brand["brand_id"]
    )

    assert result.processing.status == "draft"
    assert 0.0 <= result.processing.confidence <= 1.0


class FakeBrandBrain:
    def evaluate(self, signal, brand):
        return BrandBrainV0().evaluate(
            signal,
            brand,
        )


class FakeOpportunityEngine:
    def evaluate(
        self,
        signal,
        brand,
        brand_evaluation,
    ):
        return OpportunityEngineV0().evaluate(
            signal=signal,
            brand=brand,
            brand_evaluation=brand_evaluation,
        )


class FakeContentIdeaEngine:
    def generate(
        self,
        opportunity,
        brand,
    ):
        return ContentIdeaEngineV0().generate(
            opportunity=opportunity,
            brand=brand,
        )


def test_discovery_engine_supports_dependency_injection():
    brand = make_brand()
    signal = make_signal()

    engine = DiscoveryEngineV0(
        brand_brain=FakeBrandBrain(),
        opportunity_engine=FakeOpportunityEngine(),
        content_idea_engine=FakeContentIdeaEngine(),
    )

    result = engine.run(
        signal=signal,
        brand=brand,
    )

    assert isinstance(result, DiscoveryResult)

    assert (
        result.signal.signal_id
        == signal.signal_id
    )

    assert (
        result.opportunity.signal_id
        == signal.signal_id
    )

    assert (
        result.idea.opportunity_id
        == result.opportunity.opportunity_id
    )


def test_discovery_engine_filters_irrelevant_signal():
    brand = make_brand()
    signal = make_irrelevant_signal()

    result = DiscoveryEngineV0().run(
        signal=signal,
        brand=brand,
    )

    assert isinstance(result, DiscoveryResult)

    assert (
        result.brand_evaluation.relevant
        is False
    )

    assert (
        result.brand_evaluation.relevance_score
        == 0
    )

    assert (
        result.brand_evaluation.matched_pillars
        == []
    )

    assert (
        result.brand_evaluation.matched_topics
        == []
    )

    assert (
        result.opportunity.signal_id
        == signal.signal_id
    )

    assert (
        result.opportunity.analysis.recommendation
        == "weak_candidate"
    )

    assert result.idea is None

    assert result.processing.status == "filtered"


def test_recommendation_is_available_for_discovery_decision():
    brand = make_brand()
    signal = make_signal()

    result = DiscoveryEngineV0().run(
        signal=signal,
        brand=brand,
    )

    assert result.opportunity.analysis.recommendation in {
        "strong_candidate",
        "candidate",
        "weak_candidate",
        "reject",
    }