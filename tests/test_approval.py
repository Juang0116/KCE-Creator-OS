from src.approval.engine import ApprovalEngineV0


class MockProductionPlan:
    production_plan_id = "production_001"


class MockQAReport:
    class Summary:
        overall_status = "passed"

    qa_report_id = "qa_001"
    summary = Summary()


class MockThumbnailSource:
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
    status = "planned"


class MockThumbnailPlan:
    thumbnail_plan_id = "thumbnail_plan_001"
    source = MockThumbnailSource()
    target = MockThumbnailTarget()
    thumbnail = MockThumbnail()


class MockMetadata:
    status = "planned"


class MockMetadataPlan:
    metadata_plan_id = "metadata_plan_001"
    metadata = MockMetadata()


def create_approval_inputs(required_assets_ready=True):
    return (
        MockProductionPlan(),
        MockQAReport(),
        MockThumbnailPlan(),
        MockMetadataPlan(),
        required_assets_ready,
    )


def test_approval_engine_v0_generates_pending_approval():
    engine = ApprovalEngineV0()

    inputs = create_approval_inputs()

    result = engine.generate(*inputs)

    assert result.schema_version == "1.0"
    assert result.approval_id == "approval_001"
    assert result.approval_version == "1"

    assert result.decision.status == "pending"
    assert result.checks.approval_required is True
    assert result.processing.status == "review"


def test_approval_engine_v0_passes_ready_content():
    engine = ApprovalEngineV0()

    inputs = create_approval_inputs(required_assets_ready=True)

    result = engine.generate(*inputs)

    assert result.checks.qa_passed is True
    assert result.checks.thumbnail_ready is True
    assert result.checks.metadata_ready is True
    assert result.checks.required_assets_ready is True

    assert result.decision.status == "pending"
    assert result.decision.reason == (
        "Content package is ready for human approval."
    )

    assert result.processing.confidence == 1.0


def test_approval_engine_v0_detects_missing_assets():
    engine = ApprovalEngineV0()

    inputs = create_approval_inputs(required_assets_ready=False)

    result = engine.generate(*inputs)

    assert result.checks.qa_passed is True
    assert result.checks.thumbnail_ready is True
    assert result.checks.metadata_ready is True
    assert result.checks.required_assets_ready is False

    assert result.decision.status == "pending"
    assert result.decision.reason == (
        "Content package requires changes before approval."
    )

    assert result.processing.confidence == 0.5