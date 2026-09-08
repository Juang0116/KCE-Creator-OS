from src.metadata.engine import MetadataEngineV0


class MockThumbnailSource:
    thumbnail_plan_id = "thumbnail_plan_001"
    production_plan_id = "production_001"
    storyboard_id = "storyboard_001"
    script_id = "script_001"
    idea_id = "idea_001"
    opportunity_id = "opportunity_001"
    signal_id = "signal_001"


class MockThumbnailTarget:
    brand_id = "brand_001"
    channel = "Futuro Tech"
    platform = "YouTube"


class MockThumbnail:
    text = "The Future of AI"


class MockThumbnailPlan:
    thumbnail_plan_id = "thumbnail_plan_001"
    source = MockThumbnailSource()
    target = MockThumbnailTarget()
    thumbnail = MockThumbnail()


def test_metadata_engine_v0_generates_valid_plan():
    engine = MetadataEngineV0()

    thumbnail_plan = MockThumbnailPlan()

    result = engine.generate(thumbnail_plan)

    assert result.schema_version == "1.0"
    assert result.metadata_plan_id == "metadata_plan_001"
    assert result.metadata_plan_version == "1"

    assert result.source.thumbnail_plan_id == "thumbnail_plan_001"
    assert result.source.production_plan_id == "production_001"
    assert result.source.storyboard_id == "storyboard_001"
    assert result.source.script_id == "script_001"

    assert result.target.brand_id == "brand_001"
    assert result.target.channel == "Futuro Tech"
    assert result.target.platform == "YouTube"


def test_metadata_engine_v0_generates_metadata_content():
    engine = MetadataEngineV0()

    thumbnail_plan = MockThumbnailPlan()

    result = engine.generate(thumbnail_plan)

    metadata = result.metadata

    assert metadata.title == "The Future of AI"
    assert metadata.description
    assert metadata.keywords
    assert "The Future of AI" in metadata.keywords
    assert metadata.category == "Education"
    assert metadata.cta
    assert metadata.language == "en"
    assert metadata.status == "planned"


def test_metadata_plan_to_dict_contains_expected_structure():
    engine = MetadataEngineV0()

    thumbnail_plan = MockThumbnailPlan()

    result = engine.generate(thumbnail_plan)
    data = result.to_dict()

    assert data["schema_version"] == "1.0"
    assert data["metadata_plan_id"] == "metadata_plan_001"

    assert "source" in data
    assert "target" in data
    assert "metadata" in data
    assert "processing" in data

    assert data["metadata"]["title"] == "The Future of AI"
    assert data["metadata"]["status"] == "planned"
    assert data["processing"]["status"] == "draft"
