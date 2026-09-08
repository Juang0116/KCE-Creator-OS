import json
from pathlib import Path

from jsonschema import Draft202012Validator

from src.brand_brain import BrandBrainV0
from src.content.ideas.engine import ContentIdeaEngineV0
from src.fact_check import FactCheck
from src.fact_check.engine import FactCheckEngineV0
from src.opportunity import OpportunityEngineV0
from src.radar import RadarV0
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


def create_research():
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

    content_idea = ContentIdeaEngineV0().generate(
        opportunity,
        brand
    )

    return ResearchEngineV0().generate(
        content_idea,
        brand
    )


def create_research_with_finding():
    research = create_research()

    research.findings.append(
        type(
            "Finding",
            (),
            {
                "claim": "La GPU está diseñada para creadores.",
                "evidence": "La documentación del fabricante describe funciones orientadas a creación de contenido.",
                "source_id": "source_001",
                "confidence": 0.9,
            }
        )()
    )

    return research


def load_fact_check_schema():
    schema_path = (
        Path(__file__).resolve().parents[1]
        / "schemas"
        / "fact_check.schema.json"
    )

    with schema_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def test_generate_fact_check():
    research = create_research()

    fact_check = FactCheckEngineV0().generate(
        research
    )

    assert isinstance(fact_check, FactCheck)
    assert fact_check.fact_check_id.startswith("fact_")
    assert fact_check.research_id == research.research_id
    assert fact_check.idea_id == research.idea_id
    assert fact_check.opportunity_id == research.opportunity_id
    assert fact_check.signal_id == research.signal_id
    assert fact_check.brand_id == "futuro_tech"


def test_fact_check_starts_as_draft():
    research = create_research()

    fact_check = FactCheckEngineV0().generate(
        research
    )

    assert fact_check.processing.status == "draft"
    assert 0.0 <= fact_check.processing.confidence <= 1.0


def test_fact_check_creates_checks_from_findings():
    research = create_research_with_finding()

    fact_check = FactCheckEngineV0().generate(
        research
    )

    assert len(fact_check.checks) == 1

    check = fact_check.checks[0]

    assert check.check_id == "check_001"
    assert check.claim == "La GPU está diseñada para creadores."
    assert check.evidence
    assert check.source_ids == ["source_001"]
    assert check.verification_status == "unverified"
    assert 0.0 <= check.confidence <= 1.0

    assert fact_check.summary.total_claims == 1
    assert fact_check.summary.unverified_claims == 1
    assert fact_check.summary.verified_claims == 0


def test_fact_check_matches_schema():
    research = create_research_with_finding()

    fact_check = FactCheckEngineV0().generate(
        research
    )

    validator = Draft202012Validator(
        load_fact_check_schema()
    )

    errors = list(
        validator.iter_errors(
            fact_check.to_dict()
        )
    )

    assert errors == []