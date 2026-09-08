from src.production.engine import ProductionEngineV0


class MockSource:
    storyboard_id = "storyboard_001"
    script_id = "script_001"
    idea_id = "idea_001"
    opportunity_id = "opportunity_001"
    signal_id = "signal_001"


class MockTarget:
    brand_id = "brand_001"
    channel = "Futuro Tech"
    platform = "youtube"


class MockScene:
    def __init__(self, scene_id, section_id, duration, transition):
        self.scene_id = scene_id
        self.section_id = section_id
        self.estimated_duration_seconds = duration
        self.transition = transition


class MockStoryboard:
    storyboard_id = "storyboard_001"

    source = MockSource()
    target = MockTarget()

    scenes = [
        MockScene("scene_001", "section_001", 8, "Cut to next scene."),
        MockScene("scene_002", "section_002", 12, "Fade transition."),
    ]


class MockAsset:
    def __init__(self, asset_id, scene_id):
        self.asset_id = asset_id
        self.scene_id = scene_id


class MockAssetPlan:
    asset_plan_id = "asset_plan_001"

    assets = [
        MockAsset("asset_001", "scene_001"),
        MockAsset("asset_002", "scene_001"),
        MockAsset("asset_003", "scene_002"),
    ]


class MockVoiceSegment:
    def __init__(self, segment_id, section_id):
        self.segment_id = segment_id
        self.section_id = section_id


class MockVoicePlan:
    voice_plan_id = "voice_plan_001"

    segments = [
        MockVoiceSegment("voice_001", "section_001"),
        MockVoiceSegment("voice_002", "section_002"),
    ]


class MockMusicSFXTrack:
    def __init__(self, track_id, scene_id):
        self.track_id = track_id
        self.scene_id = scene_id


class MockMusicSFXPlan:
    music_sfx_plan_id = "music_sfx_plan_001"

    tracks = [
        MockMusicSFXTrack("music_001", "scene_001"),
        MockMusicSFXTrack("sfx_001", "scene_001"),
        MockMusicSFXTrack("music_002", "scene_002"),
    ]


def test_production_engine_v0_generates_valid_plan():
    engine = ProductionEngineV0()

    plan = engine.generate(
        MockStoryboard(),
        MockAssetPlan(),
        MockVoicePlan(),
        MockMusicSFXPlan(),
    )

    assert plan.production_plan_id == "production_plan_storyboard_001"
    assert plan.schema_version == "1.0"
    assert plan.production_plan_version == "1"
    assert plan.target.channel == "Futuro Tech"
    assert plan.target.platform == "youtube"
    assert len(plan.timeline) == 2
    assert plan.processing.status == "draft"


def test_production_engine_connects_all_source_plans():
    engine = ProductionEngineV0()

    plan = engine.generate(
        MockStoryboard(),
        MockAssetPlan(),
        MockVoicePlan(),
        MockMusicSFXPlan(),
    )

    assert plan.source.storyboard_id == "storyboard_001"
    assert plan.source.asset_plan_id == "asset_plan_001"
    assert plan.source.voice_plan_id == "voice_plan_001"
    assert plan.source.music_sfx_plan_id == "music_sfx_plan_001"
    assert plan.source.script_id == "script_001"
    assert plan.source.idea_id == "idea_001"
    assert plan.source.opportunity_id == "opportunity_001"
    assert plan.source.signal_id == "signal_001"


def test_production_timeline_maps_scene_components():
    engine = ProductionEngineV0()

    plan = engine.generate(
        MockStoryboard(),
        MockAssetPlan(),
        MockVoicePlan(),
        MockMusicSFXPlan(),
    )

    first_scene = plan.timeline[0]
    second_scene = plan.timeline[1]

    assert first_scene.scene_id == "scene_001"
    assert first_scene.start_time_seconds == 0.0
    assert first_scene.end_time_seconds == 8.0
    assert first_scene.asset_ids == ["asset_001", "asset_002"]
    assert first_scene.voice_segment_ids == ["voice_001"]
    assert first_scene.music_sfx_track_ids == ["music_001", "sfx_001"]

    assert second_scene.scene_id == "scene_002"
    assert second_scene.start_time_seconds == 8.0
    assert second_scene.end_time_seconds == 20.0
    assert second_scene.asset_ids == ["asset_003"]
    assert second_scene.voice_segment_ids == ["voice_002"]
    assert second_scene.music_sfx_track_ids == ["music_002"]