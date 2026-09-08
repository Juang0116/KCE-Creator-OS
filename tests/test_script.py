import json
from pathlib import Path

from jsonschema import Draft202012Validator

from src.script.engine import ScriptEngineV0


def test_script_engine_v0_generates_valid_script(
    sample_content_idea,
    sample_research_brief,
    sample_fact_check,
):
    engine = ScriptEngineV0()

    script = engine.generate(
        sample_content_idea,
        sample_research_brief,
        sample_fact_check,
    )

    assert script.script_id.startswith("script_")
    assert script.script_version == "1"
    assert script.processing.status == "draft"

    assert script.source.idea_id == sample_content_idea.idea_id
    assert script.source.research_id == sample_research_brief.research_id
    assert script.source.fact_check_id == sample_fact_check.fact_check_id

    assert len(script.sections) == len(sample_fact_check.checks)


def test_script_claims_preserve_fact_check_status(
    sample_content_idea,
    sample_research_brief,
    sample_fact_check,
):
    engine = ScriptEngineV0()

    script = engine.generate(
        sample_content_idea,
        sample_research_brief,
        sample_fact_check,
    )

    for section, check in zip(script.sections, sample_fact_check.checks):
        assert len(section.claims) == 1
        assert section.claims[0].claim == check.claim
        assert (
            section.claims[0].verification_status
            == check.verification_status
        )
        assert section.claims[0].fact_check_id == sample_fact_check.fact_check_id


def test_script_to_dict_matches_schema(
    sample_content_idea,
    sample_research_brief,
    sample_fact_check,
):
    engine = ScriptEngineV0()

    script = engine.generate(
        sample_content_idea,
        sample_research_brief,
        sample_fact_check,
    )

    script_dict = script.to_dict()

    schema_path = Path("schemas/script.schema.json")
    schema = json.loads(schema_path.read_text(encoding="utf-8"))

    Draft202012Validator(schema).validate(script_dict)