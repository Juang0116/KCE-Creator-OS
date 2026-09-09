from src.discovery import DiscoveryEngineV0
from src.discovery_approval import (
    DiscoveryApproval,
    DiscoveryApprovalDecision,
    DiscoveryApprovalEngineV0,
    DiscoveryApprovalProcessing,
)

from tests.test_discovery import (
    make_brand,
    make_signal,
)


def make_discovery():
    return DiscoveryEngineV0().run(
        signal=make_signal(),
        brand=make_brand(),
    )


def test_discovery_approval_decision_defaults_to_pending():
    decision = DiscoveryApprovalDecision()

    assert decision.status == "pending"
    assert decision.decided_by is None
    assert decision.decided_at is None
    assert decision.notes == ""


def test_discovery_approval_processing_defaults():
    processing = DiscoveryApprovalProcessing()

    assert processing.status == "pending"
    assert processing.confidence == 0.0
    assert processing.processed_at is None


def test_discovery_approval_engine_creates_pending_request():
    discovery = make_discovery()

    approval = DiscoveryApprovalEngineV0().generate(
        discovery
    )

    assert isinstance(
        approval,
        DiscoveryApproval,
    )

    assert approval.schema_version == "1.0"
    assert approval.approval_version == "1"

    assert (
        approval.decision.status
        == "pending"
    )

    assert (
        approval.decision.decided_by
        is None
    )

    assert (
        approval.decision.decided_at
        is None
    )

    assert (
        approval.processing.status
        == "pending"
    )


def test_discovery_approval_preserves_lineage():
    discovery = make_discovery()

    approval = DiscoveryApprovalEngineV0().generate(
        discovery
    )

    assert (
        approval.source.discovery_id
        == discovery.discovery_id
    )

    assert (
        approval.source.idea_id
        == discovery.idea.idea_id
    )

    assert (
        approval.source.opportunity_id
        == discovery.opportunity.opportunity_id
    )

    assert (
        approval.source.signal_id
        == discovery.signal.signal_id
    )


def test_discovery_approval_preserves_target():
    discovery = make_discovery()

    approval = DiscoveryApprovalEngineV0().generate(
        discovery
    )

    assert (
        approval.target.brand_id
        == discovery.idea.brand_id
    )

    assert (
        approval.target.channel
        == discovery.idea.channel
    )

    assert (
        approval.target.platform
        == discovery.idea.platform
    )


def test_discovery_approval_serialization():
    discovery = make_discovery()

    approval = DiscoveryApprovalEngineV0().generate(
        discovery
    )

    data = approval.to_dict()

    assert data["schema_version"] == "1.0"

    assert data["approval_id"].startswith(
        "discovery_approval_"
    )

    assert (
        data["source"]["discovery_id"]
        == discovery.discovery_id
    )

    assert (
        data["source"]["idea_id"]
        == discovery.idea.idea_id
    )

    assert (
        data["source"]["opportunity_id"]
        == discovery.opportunity.opportunity_id
    )

    assert (
        data["source"]["signal_id"]
        == discovery.signal.signal_id
    )

    assert (
        data["decision"]["status"]
        == "pending"
    )


def test_discovery_approval_requires_content_idea():
    discovery = make_discovery()

    discovery.idea = None

    try:
        DiscoveryApprovalEngineV0().generate(
            discovery
        )
    except ValueError as exc:
        assert (
            "without a ContentIdea"
            in str(exc)
        )
    else:
        raise AssertionError(
            "Expected ValueError"
        )