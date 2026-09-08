from src.thumbnail.engine import ThumbnailEngineV0


class MockProductionSource:
    production_plan_id = "production_001"
    storyboard_id = "storyboard_001"
    script_id = "script_001"
    idea_id = "idea_001"
    opportunity_id = "opportunity_001"
    signal_id = "signal_001"


class MockProductionTarget:
    brand_id = "brand_001"
    channel = "Futuro Tech"
    platform = "YouTube"


class MockProductionPlan:
    production_plan_id = "production_001"
    source = MockProductionSource()
    target = MockProductionTarget()
    title = "The Future of AI"


def test_thumbnail_engine_v0_generates_valid_plan():
    engine = ThumbnailEngineV0()

    production = MockProductionPlan()

    result = engine.generate(production)

    assert result.schema_version == "1.0"
    assert result.thumbnail_plan_id == "thumbnail_plan_001"
    assert result.thumbnail_plan_version == "1"

    assert result.source.production_plan_id == "production_001"
    assert result.source.storyboard_id == "storyboard_001"
    assert result.source.script_id == "script_001"

    assert result.target.brand_id == "brand_001"
    assert result.target.channel == "Futuro Tech"
    assert result.target.platform == "YouTube"


def test_thumbnail_engine_v0_generates_thumbnail_content():
    engine = ThumbnailEngineV0()

    production = MockProductionPlan()

    result = engine.generate(production)

    thumbnail = result.thumbnail

    assert thumbnail.thumbnail_id == "thumbnail_001"
    assert thumbnail.concept
    assert thumbnail.visual_direction
    assert thumbnail.text == "The Future of AI"
    assert thumbnail.composition
    assert thumbnail.status == "planned"


def test_thumbnail_plan_to_dict_contains_expected_structure():
    engine = ThumbnailEngineV0()

    production = MockProductionPlan()

    result = engine.generate(production)
    data = result.to_dict()

    assert data["schema_version"] == "1.0"
    assert data["thumbnail_plan_id"] == "thumbnail_plan_001"
    assert "source" in data
    assert "target" in data
    assert "thumbnail" in data
    assert "processing" in data

    assert data["thumbnail"]["status"] == "planned"
    assert data["processing"]["status"] == "draft"