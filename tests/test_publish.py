from src.publish.engine import PublishEngineV0


class MockApprovalDecision:
    def __init__(self, status):
        self.status = status


class MockApprovalPlan:
    approval_id = "approval_001"

    def __init__(self, status):
        self.decision = MockApprovalDecision(status)


class MockProductionPlan:
    production_plan_id = "production_001"


class MockThumbnailSource:
    storyboard_id = "storyboard_001"
    script_id = "script_001"
    idea_id = "idea_001"
    opportunity_id = "opportunity_001"
    signal_id = "signal_001"


class MockThumbnailTarget:
    brand_id = "brand_001"
    channel = "Futuro Tech"
    platform = "YouTube"


class MockThumbnailPlan:
    thumbnail_plan_id = "thumbnail_plan_001"
    source = MockThumbnailSource()
    target = MockThumbnailTarget()


class MockMetadata:
    title = "The Future of AI"
    description = "A useful exploration of the future of artificial intelligence."
    keywords = ["AI", "artificial intelligence", "Futuro Tech"]
    category = "Education"
    cta = "Subscribe for more content."
    language = "en"


class MockMetadataPlan:
    metadata_plan_id = "metadata_plan_001"
    metadata = MockMetadata()


def create_publish_inputs(approval_status):
    return (
        MockApprovalPlan(approval_status),
        MockProductionPlan(),
        MockThumbnailPlan(),
        MockMetadataPlan(),
    )


def test_publish_engine_v0_blocks_unapproved_content():
    engine = PublishEngineV0()

    inputs = create_publish_inputs("pending")

    result = engine.generate(*inputs)

    assert result.schema_version == "1.0"
    assert result.publish_plan_id == "publish_plan_001"
    assert result.publish_plan_version == "1"

    assert result.publication.status == "blocked"
    assert result.publication.visibility == "private"
    assert result.processing.status == "review"
    assert result.processing.confidence == 0.0


def test_publish_engine_v0_allows_approved_content():
    engine = PublishEngineV0()

    inputs = create_publish_inputs("approved")

    result = engine.generate(*inputs)

    assert result.publication.status == "ready"
    assert result.publication.visibility == "private"
    assert result.processing.status == "approved"
    assert result.processing.confidence == 1.0


def test_publish_engine_v0_preserves_metadata():
    engine = PublishEngineV0()

    inputs = create_publish_inputs("approved")

    result = engine.generate(*inputs)

    publication = result.publication

    assert publication.title == "The Future of AI"
    assert publication.description == (
        "A useful exploration of the future of artificial intelligence."
    )
    assert publication.keywords == [
        "AI",
        "artificial intelligence",
        "Futuro Tech",
    ]
    assert publication.category == "Education"
    assert publication.cta == "Subscribe for more content."
    assert publication.language == "en"