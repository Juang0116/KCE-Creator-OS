import json
from pathlib import Path

from jsonschema import Draft202012Validator

from src.asset.engine import AssetEngineV0
from src.script.engine import ScriptEngineV0
from src.storyboard.engine import StoryboardEngineV0


def test_asset_engine_v0_generates_valid_asset_plan(
    sample_content_idea,
    sample_research_brief,
    sample_fact_check,
):
    script = ScriptEngineV0().generate(
        sample_content_idea,
        sample_research_brief,
        sample_fact_check,
    )

    storyboard = StoryboardEngineV0().generate(script)

    engine = AssetEngineV0()
    asset_plan = engine.generate(storyboard)

    assert asset_plan.asset_plan_id.startswith("asset_plan_")
    assert asset_plan.asset_plan_version == "1"
    assert len(asset_plan.assets) >= 1
    assert asset_plan.processing.status == "draft"


def test_asset_plan_preserves_storyboard_references(
    sample_content_idea,
    sample_research_brief,
    sample_fact_check,
):
    script = ScriptEngineV0().generate(
        sample_content_idea,
        sample_research_brief,
        sample_fact_check,
    )

    storyboard = StoryboardEngineV0().generate(script)

    asset_plan = AssetEngineV0().generate(storyboard)

    assert asset_plan.source.storyboard_id == storyboard.storyboard_id
    assert asset_plan.source.script_id == storyboard.source.script_id
    assert asset_plan.source.idea_id == storyboard.source.idea_id

    assert asset_plan.target.brand_id == storyboard.target.brand_id
    assert asset_plan.target.channel == storyboard.target.channel
    assert asset_plan.target.platform == storyboard.target.platform

    storyboard_scene_ids = {
        scene.scene_id for scene in storyboard.scenes
    }

    for asset in asset_plan.assets:
        assert asset.scene_id in storyboard_scene_ids
        assert asset.required is True
        assert asset.status == "needed"


def test_asset_plan_to_dict_matches_schema(
    sample_content_idea,
    sample_research_brief,
    sample_fact_check,
):
    script = ScriptEngineV0().generate(
        sample_content_idea,
        sample_research_brief,
        sample_fact_check,
    )

    storyboard = StoryboardEngineV0().generate(script)

    asset_plan = AssetEngineV0().generate(storyboard)

    asset_plan_dict = asset_plan.to_dict()

    schema_path = Path("schemas/asset.schema.json")
    schema = json.loads(schema_path.read_text(encoding="utf-8"))

    Draft202012Validator(schema).validate(asset_plan_dict)