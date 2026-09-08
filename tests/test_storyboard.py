import json
from pathlib import Path

from jsonschema import Draft202012Validator

from src.storyboard.engine import StoryboardEngineV0


def test_storyboard_engine_v0_generates_valid_storyboard(
    sample_content_idea,
    sample_research_brief,
    sample_fact_check,
):
    from src.script.engine import ScriptEngineV0

    script_engine = ScriptEngineV0()
    script = script_engine.generate(
        sample_content_idea,
        sample_research_brief,
        sample_fact_check,
    )

    engine = StoryboardEngineV0()
    storyboard = engine.generate(script)

    assert storyboard.storyboard_id.startswith("storyboard_")
    assert storyboard.storyboard_version == "1"
    assert storyboard.metadata.scene_count == len(storyboard.scenes)
    assert len(storyboard.scenes) >= 1
    assert storyboard.processing.status == "draft"


def test_storyboard_preserves_script_content(
    sample_content_idea,
    sample_research_brief,
    sample_fact_check,
):
    from src.script.engine import ScriptEngineV0

    script_engine = ScriptEngineV0()
    script = script_engine.generate(
        sample_content_idea,
        sample_research_brief,
        sample_fact_check,
    )

    engine = StoryboardEngineV0()
    storyboard = engine.generate(script)

    assert storyboard.source.script_id == script.script_id
    assert storyboard.source.idea_id == script.source.idea_id
    assert storyboard.target.brand_id == script.target.brand_id
    assert storyboard.target.channel == script.target.channel
    assert storyboard.target.platform == script.target.platform

    assert storyboard.scenes[0].narration == script.hook.narration

    section_scene = next(
        scene
        for scene in storyboard.scenes
        if scene.section_id == script.sections[0].section_id
    )

    assert section_scene.narration == script.sections[0].narration
    assert (
        section_scene.visual_direction
        == script.sections[0].visual_direction
    )


def test_storyboard_to_dict_matches_schema(
    sample_content_idea,
    sample_research_brief,
    sample_fact_check,
):
    from src.script.engine import ScriptEngineV0

    script_engine = ScriptEngineV0()
    script = script_engine.generate(
        sample_content_idea,
        sample_research_brief,
        sample_fact_check,
    )

    engine = StoryboardEngineV0()
    storyboard = engine.generate(script)

    storyboard_dict = storyboard.to_dict()

    schema_path = Path("schemas/storyboard.schema.json")
    schema = json.loads(schema_path.read_text(encoding="utf-8"))

    Draft202012Validator(schema).validate(storyboard_dict)