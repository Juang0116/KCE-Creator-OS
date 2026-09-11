from types import SimpleNamespace

from src.orchestration import (
    ContentPipelineResult,
    ContentPipelineV0,
)


class FakeResearch:
    research_id = "research_001"


class FakeFactCheck:
    fact_check_id = "fact_check_001"


class FakeScript:
    script_id = "script_001"


class FakeVoicePlan:
    voice_plan_id = "voice_plan_001"


class FakeStoryboard:
    storyboard_id = "storyboard_001"


class FakeAssetPlan:
    asset_plan_id = "asset_plan_001"


class FakeMusicSFXPlan:
    music_sfx_plan_id = "music_sfx_plan_001"


class FakeExecution:
    execution_id = "execution_001"
    status = "awaiting_approval"


class FakeResearchEngine:
    def __init__(self, calls):
        self.calls = calls

    def generate(self, idea, brand):
        self.calls.append(("research", idea, brand))
        return FakeResearch()


class FakeFactCheckEngine:
    def __init__(self, calls):
        self.calls = calls

    def generate(self, research):
        self.calls.append(("fact_check", research))
        return FakeFactCheck()


class FakeScriptEngine:
    def __init__(self, calls):
        self.calls = calls

    def generate(
        self,
        idea,
        research,
        fact_check,
    ):
        self.calls.append(
            (
                "script",
                idea,
                research,
                fact_check,
            )
        )
        return FakeScript()


class FakeVoiceEngine:
    def __init__(self, calls):
        self.calls = calls

    def generate(self, script, voice_profile):
        self.calls.append(
            (
                "voice",
                script,
                voice_profile,
            )
        )
        return FakeVoicePlan()


class FakeStoryboardEngine:
    def __init__(self, calls):
        self.calls = calls

    def generate(self, script):
        self.calls.append(
            ("storyboard", script)
        )
        return FakeStoryboard()


class FakeAssetEngine:
    def __init__(self, calls):
        self.calls = calls

    def generate(self, storyboard):
        self.calls.append(
            ("assets", storyboard)
        )
        return FakeAssetPlan()


class FakeMusicSFXEngine:
    def __init__(self, calls):
        self.calls = calls

    def generate(self, storyboard):
        self.calls.append(
            ("music_sfx", storyboard)
        )
        return FakeMusicSFXPlan()


class FakeExecutionEngine:
    def __init__(self, calls):
        self.calls = calls

    def run(
        self,
        storyboard,
        asset_plan,
        voice_plan,
        music_sfx_plan,
    ):
        self.calls.append(
            (
                "execution",
                storyboard,
                asset_plan,
                voice_plan,
                music_sfx_plan,
            )
        )
        return FakeExecution()


def make_discovery_package(
    approval_status="approved",
):
    idea = SimpleNamespace(
        idea_id="idea_001",
        opportunity_id="opportunity_001",
        signal_id="signal_001",
    )

    discovery = SimpleNamespace(
        discovery_id="discovery_001",
        idea=idea,
        opportunity=SimpleNamespace(
            opportunity_id="opportunity_001",
            signal_id="signal_001",
        ),
    )

    approval = SimpleNamespace(
        approval_id="discovery_approval_001",
        decision=SimpleNamespace(
            status=approval_status,
        ),
    )

    return SimpleNamespace(
        discovery=discovery,
        approval=approval,
    )


def make_pipeline(calls):
    return ContentPipelineV0(
        research_engine=FakeResearchEngine(calls),
        fact_check_engine=FakeFactCheckEngine(calls),
        script_engine=FakeScriptEngine(calls),
        voice_engine=FakeVoiceEngine(calls),
        storyboard_engine=FakeStoryboardEngine(calls),
        asset_engine=FakeAssetEngine(calls),
        music_sfx_engine=FakeMusicSFXEngine(calls),
        execution_engine=FakeExecutionEngine(calls),
    )


def test_pipeline_blocks_when_discovery_is_not_approved():
    calls = []

    pipeline = make_pipeline(calls)

    result = pipeline.run(
        discovery_package=make_discovery_package(
            approval_status="pending"
        ),
        brand={"brand_id": "futuro_tech"},
        voice_profile=SimpleNamespace(
            voice_id="voice_001"
        ),
    )

    assert isinstance(
        result,
        ContentPipelineResult,
    )

    assert result.status == "blocked"

    assert len(result.stages) == 1

    assert (
        result.stages[0].name
        == "discovery_approval"
    )

    assert (
        result.stages[0].status
        == "blocked"
    )

    assert (
        result.stages[0].artifact_id
        == "discovery_approval_001"
    )

    assert calls == []


def test_pipeline_blocks_when_discovery_approval_is_missing():
    calls = []

    pipeline = make_pipeline(calls)

    package = make_discovery_package(
        approval_status="approved"
    )

    package.approval = None

    result = pipeline.run(
        discovery_package=package,
        brand={"brand_id": "futuro_tech"},
        voice_profile=SimpleNamespace(
            voice_id="voice_001"
        ),
    )

    assert result.status == "blocked"

    assert (
        result.stages[0].name
        == "discovery_approval"
    )

    assert (
        result.stages[0].status
        == "blocked"
    )

    assert calls == []


def test_pipeline_orchestrates_all_content_stages_in_order():
    calls = []

    pipeline = make_pipeline(calls)

    result = pipeline.run(
        discovery_package=make_discovery_package(),
        brand={"brand_id": "futuro_tech"},
        voice_profile=SimpleNamespace(
            voice_id="voice_001"
        ),
    )

    assert result.status == "awaiting_approval"

    assert [
        call[0]
        for call in calls
    ] == [
        "research",
        "fact_check",
        "script",
        "voice",
        "storyboard",
        "assets",
        "music_sfx",
        "execution",
    ]


def test_pipeline_preserves_artifacts_and_lineage():
    calls = []

    pipeline = make_pipeline(calls)

    result = pipeline.run(
        discovery_package=make_discovery_package(),
        brand={"brand_id": "futuro_tech"},
        voice_profile=SimpleNamespace(
            voice_id="voice_001"
        ),
    )

    assert (
        result.lineage.discovery_id
        == "discovery_001"
    )

    assert (
        result.lineage.signal_id
        == "signal_001"
    )

    assert (
        result.lineage.opportunity_id
        == "opportunity_001"
    )

    assert (
        result.lineage.idea_id
        == "idea_001"
    )

    assert (
        result.lineage.research_id
        == "research_001"
    )

    assert (
        result.lineage.fact_check_id
        == "fact_check_001"
    )

    assert (
        result.lineage.script_id
        == "script_001"
    )

    assert (
        result.lineage.voice_plan_id
        == "voice_plan_001"
    )

    assert (
        result.lineage.storyboard_id
        == "storyboard_001"
    )

    assert (
        result.lineage.asset_plan_id
        == "asset_plan_001"
    )

    assert (
        result.lineage.music_sfx_plan_id
        == "music_sfx_plan_001"
    )

    assert (
        result.lineage.execution_id
        == "execution_001"
    )

    assert (
        result.artifacts.research.research_id
        == "research_001"
    )

    assert (
        result.artifacts.fact_check.fact_check_id
        == "fact_check_001"
    )

    assert (
        result.artifacts.script.script_id
        == "script_001"
    )

    assert (
        result.artifacts.voice_plan.voice_plan_id
        == "voice_plan_001"
    )

    assert (
        result.artifacts.storyboard.storyboard_id
        == "storyboard_001"
    )

    assert (
        result.artifacts.asset_plan.asset_plan_id
        == "asset_plan_001"
    )

    assert (
        result.artifacts.music_sfx_plan
        .music_sfx_plan_id
        == "music_sfx_plan_001"
    )

    assert (
        result.artifacts.execution.execution_id
        == "execution_001"
    )


def test_pipeline_records_expected_stage_states():
    calls = []

    pipeline = make_pipeline(calls)

    result = pipeline.run(
        discovery_package=make_discovery_package(),
        brand={"brand_id": "futuro_tech"},
        voice_profile=SimpleNamespace(
            voice_id="voice_001"
        ),
    )

    assert [
        stage.name
        for stage in result.stages
    ] == [
        "discovery_approval",
        "research",
        "fact_check",
        "script",
        "voice",
        "storyboard",
        "assets",
        "music_sfx",
        "execution",
    ]

    assert all(
        stage.status == "completed"
        for stage in result.stages[0:8]
    )

    assert (
        result.stages[-1].status
        == "waiting"
    )

    assert (
        result.stages[-1].message
        == "awaiting_approval"
    )


def test_pipeline_passes_previous_artifacts_to_next_stage():
    calls = []

    pipeline = make_pipeline(calls)

    package = make_discovery_package()

    brand = {
        "brand_id": "futuro_tech",
    }

    voice_profile = SimpleNamespace(
        voice_id="voice_001"
    )

    result = pipeline.run(
        discovery_package=package,
        brand=brand,
        voice_profile=voice_profile,
    )

    research = result.artifacts.research
    fact_check = result.artifacts.fact_check
    script = result.artifacts.script
    storyboard = result.artifacts.storyboard
    asset_plan = result.artifacts.asset_plan
    music_sfx_plan = (
        result.artifacts.music_sfx_plan
    )
    voice_plan = result.artifacts.voice_plan

    assert calls[0][0] == "research"
    assert calls[0][1] is package.discovery.idea
    assert calls[0][2] is brand

    assert calls[1][0] == "fact_check"
    assert calls[1][1] is research

    assert calls[2][0] == "script"
    assert calls[2][1] is package.discovery.idea
    assert calls[2][2] is research
    assert calls[2][3] is fact_check

    assert calls[3][0] == "voice"
    assert calls[3][1] is script
    assert calls[3][2] is voice_profile

    assert calls[4][0] == "storyboard"
    assert calls[4][1] is script

    assert calls[5][0] == "assets"
    assert calls[5][1] is storyboard

    assert calls[6][0] == "music_sfx"
    assert calls[6][1] is storyboard

    assert calls[7][0] == "execution"
    assert calls[7][1] is storyboard
    assert calls[7][2] is asset_plan
    assert calls[7][3] is voice_plan
    assert calls[7][4] is music_sfx_plan