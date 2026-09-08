import json
from pathlib import Path

from jsonschema import Draft202012Validator

from src.brand_brain import BrandBrainV0
from src.content.ideas import ContentIdea
from src.content.ideas.engine import ContentIdeaEngineV0
from src.opportunity import OpportunityEngineV0
from src.radar import RadarV0


def create_signal():
    raw_signal = {
        "source_type": "news",
        "platform": "TestPlatform",
        "title": "Nueva GPU revolucionaria para creadores",
        "summary": "Una nueva GPU genera interés entre creadores.",
        "keywords": [
            "GPU",
            "AI",
            "PC",
            "creators",
        ],
        "topics": [
            "technology",
            "AI",
            "GPU",
        ],
        "language": "es",
        "evidence": {
            "engagement": {
                "views": 1_500_000,
                "likes": 80_000,
                "comments": 12_000,
                "shares": 5_000,
            },
            "observations": [],
        },
    }

    return RadarV0().collect([raw_signal])[0]


def create_brand():
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
            "target": "Creadores de contenido interesados en tecnología.",
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


def create_opportunity():
    signal = create_signal()
    brand = create_brand()

    evaluation = BrandBrainV0().evaluate(
        signal,
        brand,
    )

    return OpportunityEngineV0().evaluate(
        signal,
        brand,
        evaluation,
    )


def load_content_idea_schema():
    schema_path = (
        Path(__file__).resolve().parents[1]
        / "schemas"
        / "content_idea.schema.json"
    )

    with schema_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def test_generate_content_idea():
    opportunity = create_opportunity()
    brand = create_brand()

    idea = ContentIdeaEngineV0().generate(
        opportunity,
        brand,
    )

    assert isinstance(idea, ContentIdea)
    assert idea.idea_id.startswith("idea_")
    assert idea.opportunity_id == opportunity.opportunity_id
    assert idea.signal_id == opportunity.signal_id
    assert idea.brand_id == "futuro_tech"


def test_content_idea_starts_as_draft():
    opportunity = create_opportunity()
    brand = create_brand()

    idea = ContentIdeaEngineV0().generate(
        opportunity,
        brand,
    )

    assert idea.processing.status == "draft"
    assert 0.0 <= idea.processing.confidence <= 1.0


def test_content_idea_has_required_components():
    opportunity = create_opportunity()
    brand = create_brand()

    idea = ContentIdeaEngineV0().generate(
        opportunity,
        brand,
    )

    assert idea.concept.working_title
    assert idea.concept.hook
    assert idea.concept.core_promise
    assert idea.concept.angle
    assert idea.concept.format
    assert idea.concept.estimated_duration_seconds > 0
    assert idea.concept.content_pillar

    assert idea.audience.target
    assert idea.audience.audience_need
    assert idea.audience.expected_value

    assert idea.creative_direction.storytelling_approach
    assert idea.creative_direction.visual_direction
    assert idea.creative_direction.voice_direction
    assert idea.creative_direction.key_elements

    assert idea.production.complexity
    assert idea.production.estimated_production_hours > 0
    assert idea.production.required_assets
    assert idea.production.ai_assistance


def test_content_idea_matches_schema():
    opportunity = create_opportunity()
    brand = create_brand()

    idea = ContentIdeaEngineV0().generate(
        opportunity,
        brand,
    )

    validator = Draft202012Validator(
        load_content_idea_schema()
    )

    errors = list(
        validator.iter_errors(
            idea.to_dict()
        )
    )

    assert errors == []