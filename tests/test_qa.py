from src.qa.engine import QAEngineV0


class MockProductionSource:
    storyboard_id = "storyboard_001"
    asset_plan_id = "asset_plan_001"
    voice_plan_id = "voice_plan_001"
    music_sfx_plan_id = "music_sfx_plan_001"
    script_id = "script_001"
    idea_id = "idea_001"
    opportunity_id = "opportunity_001"
    signal_id = "signal_001"


class MockProductionItem:
    def __init__(
        self,
        timeline_id,
        scene_id,
        start,
        end,
        asset_ids,
        voice_ids,
        audio_ids,
    ):
        self.timeline_id = timeline_id
        self.scene_id = scene_id
        self.start_time_seconds = start
        self.end_time_seconds = end
        self.asset_ids = asset_ids
        self.voice_segment_ids = voice_ids
        self.music_sfx_track_ids = audio_ids


class MockProductionPlan:
    def __init__(self):
        self.production_plan_id = "production_001"
        self.source = MockProductionSource()

        self.timeline = [
            MockProductionItem(
                "timeline_001",
                "scene_001",
                0.0,
                8.0,
                ["asset_001"],
                ["voice_001"],
                ["music_001"],
            ),
            MockProductionItem(
                "timeline_002",
                "scene_002",
                8.0,
                20.0,
                ["asset_002"],
                ["voice_002"],
                ["music_002"],
            ),
        ]


class MockAsset:
    def __init__(self, asset_id):
        self.asset_id = asset_id


class MockAssetPlan:
    asset_plan_id = "asset_plan_001"

    assets = [
        MockAsset("asset_001"),
        MockAsset("asset_002"),
    ]


class MockVoiceSegment:
    def __init__(self, segment_id):
        self.segment_id = segment_id


class MockVoicePlan:
    voice_plan_id = "voice_plan_001"

    segments = [
        MockVoiceSegment("voice_001"),
        MockVoiceSegment("voice_002"),
    ]


class MockMusicSFXTrack:
    def __init__(self, track_id):
        self.track_id = track_id


class MockMusicSFXPlan:
    music_sfx_plan_id = "music_sfx_plan_001"

    tracks = [
        MockMusicSFXTrack("music_001"),
        MockMusicSFXTrack("music_002"),
    ]


def test_qa_engine_v0_generates_valid_report():
    engine = QAEngineV0()

    report = engine.generate(
        MockProductionPlan(),
        MockAssetPlan(),
        MockVoicePlan(),
        MockMusicSFXPlan(),
    )

    assert report.qa_report_id == "qa_report_production_001"
    assert report.schema_version == "1.0"
    assert report.qa_version == "1"
    assert report.summary.total_checks == 6
    assert report.summary.passed == 6
    assert report.summary.warnings == 0
    assert report.summary.failed == 0
    assert report.summary.overall_status == "passed"
    assert report.processing.status == "approved"


def test_qa_engine_detects_missing_asset_reference():
    engine = QAEngineV0()

    production = MockProductionPlan()

    production.timeline[0].asset_ids = [
        "asset_missing"
    ]

    report = engine.generate(
        production,
        MockAssetPlan(),
        MockVoicePlan(),
        MockMusicSFXPlan(),
    )

    asset_check = next(
        check
        for check in report.checks
        if check.check_id == "check_asset_references"
    )

    assert asset_check.status == "failed"
    assert asset_check.severity == "high"
    assert "asset_missing" in asset_check.message
    assert report.summary.failed == 1
    assert report.summary.overall_status == "failed"
    assert report.processing.status == "review"


def test_qa_report_to_dict_contains_expected_structure():
    engine = QAEngineV0()

    report = engine.generate(
        MockProductionPlan(),
        MockAssetPlan(),
        MockVoicePlan(),
        MockMusicSFXPlan(),
    )

    data = report.to_dict()

    assert "schema_version" in data
    assert "qa_report_id" in data
    assert "source" in data
    assert "checks" in data
    assert "summary" in data
    assert "processing" in data

    assert len(data["checks"]) == 6
    assert data["summary"]["overall_status"] == "passed"