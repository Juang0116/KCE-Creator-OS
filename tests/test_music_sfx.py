from src.music_sfx.engine import MusicSFXEngineV0


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
    def __init__(self, scene_id, duration, transition):
        self.scene_id = scene_id
        self.estimated_duration_seconds = duration
        self.transition = transition


class MockStoryboard:
    storyboard_id = "storyboard_001"

    source = MockSource()
    target = MockTarget()

    scenes = [
        MockScene("scene_001", 8, "Cut to next scene."),
        MockScene("scene_002", 12, "Fade transition."),
        MockScene("scene_003", 10, ""),
    ]


def test_music_sfx_engine_v0_generates_valid_plan():
    engine = MusicSFXEngineV0()

    storyboard = MockStoryboard()

    plan = engine.generate(storyboard)

    assert plan.music_sfx_plan_id == "music_sfx_plan_storyboard_001"
    assert plan.schema_version == "1.0"
    assert plan.music_sfx_plan_version == "1"
    assert plan.target.channel == "Futuro Tech"
    assert plan.target.platform == "youtube"
    assert len(plan.tracks) == 5
    assert plan.processing.status == "draft"


def test_music_sfx_engine_preserves_storyboard_references():
    engine = MusicSFXEngineV0()

    storyboard = MockStoryboard()

    plan = engine.generate(storyboard)

    assert plan.source.storyboard_id == "storyboard_001"
    assert plan.source.script_id == "script_001"
    assert plan.source.idea_id == "idea_001"
    assert plan.source.opportunity_id == "opportunity_001"
    assert plan.source.signal_id == "signal_001"


def test_music_sfx_plan_to_dict_contains_expected_structure():
    engine = MusicSFXEngineV0()

    storyboard = MockStoryboard()

    plan = engine.generate(storyboard)

    data = plan.to_dict()

    assert "schema_version" in data
    assert "music_sfx_plan_id" in data
    assert "source" in data
    assert "target" in data
    assert "tracks" in data
    assert "processing" in data

    assert len(data["tracks"]) == 5