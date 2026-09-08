import json
from pathlib import Path

from jsonschema import Draft202012Validator

from src.brand_brain import BrandBrainV0
from src.content.ideas.engine import ContentIdeaEngineV0
from src.opportunity import OpportunityEngineV0
from src.radar import RadarV0
from src.research import ResearchBrief
from src.research.engine import ResearchEngineV0


def create_signal():
    raw_signal = {
        "source_type": "news",
        "platform": "TestPlatform",
        "title": "Nueva GPU revolucionaria para creadores",
        "summary": "Una nueva GPU genera interés entre creadores.",
        "keywords": ["GPU", "AI", "PC", "creators"],
        "topics": ["technology", "AI", "GPU"],
        "language": "es",
        "evidence": {
            "engagement": {
                "views": 1500000,
                "likes": 80000,
                "comments": 12000,
                "shares": 5000
            },
            "observations": []
        }
    }

    return RadarV0().collect([raw_signal])[0]


def create_brand():
    return {
        "brand_id": "futuro_tech",
        "content": {
            "pillars": ["technology", "AI", "hardware", "PC"],
            "topics": ["GPU", "AI", "creators"]
        },
        "audience": {
            "target": "Creadores de contenido interesados en tecnología.",
            "interests": ["GPU", "AI", "PC"]
        },
        "channels_community": {
            "primary_platforms": ["YouTube"]
        }
    }


def create_content_idea():
    signal = create_signal()
    brand = create_brand()

    evaluation = BrandBrainV0().evaluate(
        signal,
        brand
    )

    opportunity = OpportunityEngineV0().evaluate(
        signal,
        brand,
        evaluation
    )

    return ContentIdeaEngineV0().generate(
        opportunity,
        brand
    )


def load_research_brief_schema():
    schema_path = (
        Path(__file__).resolve().parents[1]
        / "schemas"
        / "research_brief.schema.json"
    )

    with schema_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def test_generate_research_brief():
    content_idea = create_content_idea()
    brand = create_brand()

    research = ResearchEngineV0().generate(
        content_idea,
        brand
    )

    assert isinstance(research, ResearchBrief)
    assert research.research_id.startswith("research_")
    assert research.idea_id == content_idea.idea_id
    assert research.opportunity_id == content_idea.opportunity_id
    assert research.signal_id == content_idea.signal_id
    assert research.brand_id == "futuro_tech"


def test_research_starts_as_draft():
    content_idea = create_content_idea()
    brand = create_brand()

    research = ResearchEngineV0().generate(
        content_idea,
        brand
    )

    assert research.processing.status == "draft"
    assert 0.0 <= research.processing.confidence <= 1.0


def test_research_has_objective_and_scope():
    content_idea = create_content_idea()
    brand = create_brand()

    research = ResearchEngineV0().generate(
        content_idea,
        brand
    )

    assert research.objective.research_question
    assert research.objective.content_goal
    assert research.objective.key_questions

    assert research.scope.topics
    assert research.scope.keywords
    assert research.scope.exclusions


def test_research_matches_schema():
    content_idea = create_content_idea()
    brand = create_brand()

    research = ResearchEngineV0().generate(
        content_idea,
        brand
    )

    validator = Draft202012Validator(
        load_research_brief_schema()
    )

    errors = list(
        validator.iter_errors(
            research.to_dict()
        )
    )

    assert errors == []