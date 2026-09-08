from src.asset.engine import AssetEngineV0
from src.script.engine import ScriptEngineV0
from src.storyboard.engine import StoryboardEngineV0


def build_storyboard(
    sample_content_idea,
    sample_research_brief,
    sample_fact_check,
):
    script = ScriptEngineV0().generate(
        sample_content_idea,
        sample_research_brief,
        sample_fact_check,
    )

    return StoryboardEngineV0().generate(script)


def test_storyboard_visual_assets_become_asset_requirements(
    sample_content_idea,
    sample_research_brief,
    sample_fact_check,
):
    storyboard = build_storyboard(
        sample_content_idea,
        sample_research_brief,
        sample_fact_check,
    )

    asset_plan = AssetEngineV0().generate(storyboard)

    expected_assets = sum(
        len(scene.visual_assets)
        for scene in storyboard.scenes
    )

    assert len(asset_plan.assets) == expected_assets

    for scene in storyboard.scenes:
        scene_assets = [
            asset
            for asset in asset_plan.assets
            if asset.scene_id == scene.scene_id
        ]

        assert len(scene_assets) == len(scene.visual_assets)

        for asset, visual_asset in zip(
            scene_assets,
            scene.visual_assets,
        ):
            assert asset.description == visual_asset


def test_asset_requirements_preserve_scene_mapping(
    sample_content_idea,
    sample_research_brief,
    sample_fact_check,
):
    storyboard = build_storyboard(
        sample_content_idea,
        sample_research_brief,
        sample_fact_check,
    )

    asset_plan = AssetEngineV0().generate(storyboard)

    storyboard_scene_ids = {
        scene.scene_id
        for scene in storyboard.scenes
    }

    for asset in asset_plan.assets:
        assert asset.scene_id in storyboard_scene_ids
        assert asset.required is True
        assert asset.status == "needed"


def test_asset_type_and_source_strategy_inference():
    engine = AssetEngineV0()

    assert engine._infer_asset_type("screenshot") == "screenshot"
    assert engine._infer_asset_type("video clip") == "video"
    assert engine._infer_asset_type("background") == "background"
    assert engine._infer_asset_type("icon") == "icon"
    assert engine._infer_asset_type("intro_graphics") == "graphic"
    assert engine._infer_asset_type("audio") == "audio"
    assert engine._infer_asset_type("text overlay") == "text"
    assert engine._infer_asset_type("character image") == "image"

    assert engine._infer_source_strategy("image") == "retrieve"
    assert engine._infer_source_strategy("video") == "retrieve"
    assert engine._infer_source_strategy("graphic") == "create"
    assert engine._infer_source_strategy("screenshot") == "capture"
    assert engine._infer_source_strategy("background") == "generate"
    assert engine._infer_source_strategy("icon") == "retrieve"
    assert engine._infer_source_strategy("text") == "create"
    assert engine._infer_source_strategy("audio") == "generate"
    assert engine._infer_source_strategy("other") == "create"


def test_asset_plan_preserves_complete_storyboard_lineage(
    sample_content_idea,
    sample_research_brief,
    sample_fact_check,
):
    storyboard = build_storyboard(
        sample_content_idea,
        sample_research_brief,
        sample_fact_check,
    )

    asset_plan = AssetEngineV0().generate(storyboard)

    assert asset_plan.source.storyboard_id == storyboard.storyboard_id
    assert asset_plan.source.script_id == storyboard.source.script_id
    assert asset_plan.source.idea_id == storyboard.source.idea_id
    assert (
        asset_plan.source.opportunity_id
        == storyboard.source.opportunity_id
    )
    assert asset_plan.source.signal_id == storyboard.source.signal_id

    assert asset_plan.target.brand_id == storyboard.target.brand_id
    assert asset_plan.target.channel == storyboard.target.channel
    assert asset_plan.target.platform == storyboard.target.platform
