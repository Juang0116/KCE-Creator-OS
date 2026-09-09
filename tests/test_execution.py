from types import SimpleNamespace

from src.approval.engine import ApprovalEngineV0
from src.execution.engine import ExecutionEngineV0


def make_storyboard(duration=10):
    scene = SimpleNamespace(
        scene_id="scene_001",
        section_id="section_001",
        estimated_duration_seconds=duration,
        transition="fade",
    )

    source = SimpleNamespace(
        storyboard_id="storyboard_001",
        script_id="script_001",
        idea_id="idea_001",
        opportunity_id="opportunity_001",
        signal_id="signal_001",
    )

    target = SimpleNamespace(
        brand_id="brand_001",
        channel="Test Channel",
        platform="youtube",
    )

    return SimpleNamespace(
        storyboard_id="storyboard_001",
        source=source,
        target=target,
        scenes=[scene],
        metadata=SimpleNamespace(
            title="Execution Test",
            format="long_form",
            estimated_duration_seconds=10,
        ),
        processing=SimpleNamespace(
            status="draft",
            confidence=1.0,
        ),
    )


def make_asset_plan():
    asset = SimpleNamespace(
        asset_id="asset_001",
        scene_id="scene_001",
        asset_type="image",
        status="planned",
        required=True,
    )

    return SimpleNamespace(
        asset_plan_id="asset_plan_storyboard_001",
        source=SimpleNamespace(
            storyboard_id="storyboard_001",
            script_id="script_001",
            idea_id="idea_001",
            opportunity_id="opportunity_001",
            signal_id="signal_001",
        ),
        target=SimpleNamespace(
            brand_id="brand_001",
            channel="Test Channel",
            platform="youtube",
        ),
        assets=[asset],
    )


def make_voice_plan():
    segment = SimpleNamespace(
        segment_id="voice_001",
        section_id="section_001",
    )

    return SimpleNamespace(
        voice_plan_id="voice_plan_script_001",
        source=SimpleNamespace(
            script_id="script_001",
            storyboard_id="",
            idea_id="idea_001",
            opportunity_id="opportunity_001",
            signal_id="signal_001",
        ),
        target=SimpleNamespace(
            brand_id="brand_001",
            channel="Test Channel",
            platform="youtube",
        ),
        segments=[segment],
    )


def make_music_sfx_plan():
    track = SimpleNamespace(
        track_id="music_001",
        scene_id="scene_001",
    )

    return SimpleNamespace(
        music_sfx_plan_id="music_sfx_plan_storyboard_001",
        source=SimpleNamespace(
            storyboard_id="storyboard_001",
            script_id="script_001",
            idea_id="idea_001",
            opportunity_id="opportunity_001",
            signal_id="signal_001",
        ),
        target=SimpleNamespace(
            brand_id="brand_001",
            channel="Test Channel",
            platform="youtube",
        ),
        tracks=[track],
    )


def make_inputs(duration=10):
    return (
        make_storyboard(duration),
        make_asset_plan(),
        make_voice_plan(),
        make_music_sfx_plan(),
    )


def test_execution_stops_when_qa_fails():
    storyboard, asset_plan, voice_plan, music_sfx_plan = make_inputs(
        duration=0
    )

    engine = ExecutionEngineV0()

    result = engine.run(
        storyboard=storyboard,
        asset_plan=asset_plan,
        voice_plan=voice_plan,
        music_sfx_plan=music_sfx_plan,
    )

    assert result.status == "qa_failed"

    stage_names = [stage.name for stage in result.stages]

    assert stage_names == ["production", "qa"]

    qa_stage = result.stages[-1]

    assert qa_stage.status == "failed"


def test_execution_waits_for_human_approval():
    storyboard, asset_plan, voice_plan, music_sfx_plan = make_inputs()

    engine = ExecutionEngineV0()

    result = engine.run(
        storyboard=storyboard,
        asset_plan=asset_plan,
        voice_plan=voice_plan,
        music_sfx_plan=music_sfx_plan,
    )

    assert result.status == "awaiting_approval"

    stage_names = [stage.name for stage in result.stages]

    assert stage_names == [
        "production",
        "qa",
        "thumbnail",
        "metadata",
        "approval",
        "publish",
    ]

    approval_stage = result.stages[-2]
    publish_stage = result.stages[-1]

    assert approval_stage.status == "waiting"
    assert approval_stage.message == "pending"

    assert publish_stage.status == "blocked"


class ApprovedApprovalEngine:
    def generate(
        self,
        production_plan,
        qa_report,
        thumbnail_plan,
        metadata_plan,
        required_assets_ready=True,
    ):
        approval_plan = ApprovalEngineV0().generate(
            production_plan=production_plan,
            qa_report=qa_report,
            thumbnail_plan=thumbnail_plan,
            metadata_plan=metadata_plan,
            required_assets_ready=required_assets_ready,
        )

        approval_plan.decision.status = "approved"
        approval_plan.decision.approved_by = "test"
        approval_plan.decision.approved_at = "2026-01-01T00:00:00+00:00"

        return approval_plan


def test_execution_reaches_ready_to_publish_after_approval():
    storyboard, asset_plan, voice_plan, music_sfx_plan = make_inputs()

    engine = ExecutionEngineV0(
        approval_engine=ApprovedApprovalEngine()
    )

    result = engine.run(
        storyboard=storyboard,
        asset_plan=asset_plan,
        voice_plan=voice_plan,
        music_sfx_plan=music_sfx_plan,
    )

    assert result.status == "ready_to_publish"

    approval_stage = result.stages[-2]
    publish_stage = result.stages[-1]

    assert approval_stage.status == "completed"
    assert approval_stage.message == "approved"

    assert publish_stage.status == "completed"
    assert publish_stage.message == "ready"


def test_execution_preserves_lineage():
    storyboard, asset_plan, voice_plan, music_sfx_plan = make_inputs()

    engine = ExecutionEngineV0()

    result = engine.run(
        storyboard=storyboard,
        asset_plan=asset_plan,
        voice_plan=voice_plan,
        music_sfx_plan=music_sfx_plan,
    )

    assert result.lineage.storyboard_id == "storyboard_001"
    assert result.lineage.script_id == "script_001"
    assert result.lineage.idea_id == "idea_001"
    assert result.lineage.opportunity_id == "opportunity_001"
    assert result.lineage.signal_id == "signal_001"