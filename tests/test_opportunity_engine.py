import json
from pathlib import Path

from jsonschema import Draft202012Validator

from src.brand_brain import BrandBrainV0
from src.opportunity import OpportunityEngineV0
from src.radar import RadarV0


def create_signal(
    title: str,
    keywords: list[str],
    topics: list[str],
    source_type: str = "news",
    engagement: dict | None = None,
):
    raw_signal = {
        "source_type": source_type,
        "platform": "TestPlatform",
        "title": title,
        "summary": "Señal de prueba para Opportunity Engine.",
        "keywords": keywords,
        "topics": topics,
        "language": "es",
        "evidence": {
            "engagement": engagement or {},
            "observations": [],
        },
    }

    return RadarV0().collect([raw_signal])[0]


def create_futuro_tech_brand():
    return {
        "brand_id": "futuro_tech",
        "content": {
            "pillars": [
                "technology",
                "AI",
                "hardware",
                "PC",
            ],
            "topics": [
                "GPU",
                "AI",
                "creators",
            ],
        },
        "audience": {
            "interests": [
                "GPU",
                "AI",
                "PC",
            ],
        },
        "channels_community": {
            "primary_platforms": [
                "YouTube",
            ],
        },
    }


def load_opportunity_schema():
    schema_path = (
        Path(__file__).resolve().parents[1]
        / "schemas"
        / "opportunity.schema.json"
    )

    with schema_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def test_strong_opportunity():
    signal = create_signal(
        title="Nueva GPU revolucionaria para creadores",
        keywords=[
            "GPU",
            "AI",
            "PC",
            "creators",
        ],
        topics=[
            "technology",
            "AI",
            "GPU",
        ],
        engagement={
            "views": 1_500_000,
            "likes": 80_000,
            "comments": 12_000,
            "shares": 5_000,
        },
    )

    brand = create_futuro_tech_brand()

    evaluation = BrandBrainV0().evaluate(
        signal,
        brand,
    )

    opportunity = OpportunityEngineV0().evaluate(
        signal,
        brand,
        evaluation,
    )

    assert opportunity.scoring.total_score >= 80
    assert opportunity.analysis.recommendation == "strong_candidate"
    assert opportunity.processing.status == "evaluated"


def test_weak_opportunity():
    signal = create_signal(
        title="Resultado de un partido de fútbol",
        keywords=[
            "football",
            "match",
        ],
        topics=[
            "football",
            "sports",
        ],
    )

    brand = create_futuro_tech_brand()

    evaluation = BrandBrainV0().evaluate(
        signal,
        brand,
    )

    opportunity = OpportunityEngineV0().evaluate(
        signal,
        brand,
        evaluation,
    )

    assert opportunity.scoring.relevance == 0
    assert opportunity.scoring.total_score < 60
    assert opportunity.analysis.recommendation in {
        "weak_candidate",
        "reject",
    }


def test_opportunity_matches_schema():
    signal = create_signal(
        title="Nueva tecnología para creadores",
        keywords=[
            "AI",
            "GPU",
        ],
        topics=[
            "technology",
            "AI",
        ],
    )

    brand = create_futuro_tech_brand()

    evaluation = BrandBrainV0().evaluate(
        signal,
        brand,
    )

    opportunity = OpportunityEngineV0().evaluate(
        signal,
        brand,
        evaluation,
    )

    validator = Draft202012Validator(
        load_opportunity_schema()
    )

    errors = list(
        validator.iter_errors(
            opportunity.to_dict()
        )
    )

    assert errors == []