from src.discovery import DiscoveryEngineV0
from src.discovery_approval import DiscoveryApprovalEngineV0
from src.orchestration import (
    DiscoveryPackage,
    DiscoveryWorkflowV0,
)

from tests.test_discovery import (
    make_brand,
    make_irrelevant_signal,
    make_signal,
)


def test_discovery_workflow_generates_complete_package():
    brand = make_brand()
    signal = make_signal()

    workflow = DiscoveryWorkflowV0()

    package = workflow.run(
        signal=signal,
        brand=brand,
    )

    assert isinstance(
        package,
        DiscoveryPackage,
    )

    assert package.discovery is not None
    assert package.approval is not None

    assert (
        package.discovery.signal.signal_id
        == signal.signal_id
    )

    assert (
        package.discovery.opportunity.signal_id
        == signal.signal_id
    )

    assert (
        package.discovery.idea.signal_id
        == signal.signal_id
    )

    assert (
        package.approval.source.discovery_id
        == package.discovery.discovery_id
    )

    assert (
        package.approval.source.idea_id
        == package.discovery.idea.idea_id
    )

    assert (
        package.approval.source.opportunity_id
        == package.discovery.opportunity.opportunity_id
    )

    assert (
        package.approval.source.signal_id
        == signal.signal_id
    )


def test_discovery_workflow_creates_pending_approval():
    brand = make_brand()
    signal = make_signal()

    package = DiscoveryWorkflowV0().run(
        signal=signal,
        brand=brand,
    )

    assert package.approval is not None

    assert (
        package.approval.decision.status
        == "pending"
    )

    assert (
        package.approval.decision.decided_by
        is None
    )

    assert (
        package.approval.decision.decided_at
        is None
    )


def test_discovery_workflow_does_not_create_approval_when_filtered():
    brand = make_brand()
    signal = make_irrelevant_signal()

    package = DiscoveryWorkflowV0().run(
        signal=signal,
        brand=brand,
    )

    assert package.discovery is not None

    assert (
        package.discovery.processing.status
        == "filtered"
    )

    assert package.discovery.idea is None

    assert package.approval is None


def test_discovery_workflow_serialization():
    brand = make_brand()
    signal = make_signal()

    package = DiscoveryWorkflowV0().run(
        signal=signal,
        brand=brand,
    )

    data = package.to_dict()

    assert "discovery" in data
    assert "approval" in data

    assert (
        data["discovery"]["signal"]["signal_id"]
        == signal.signal_id
    )

    assert (
        data["discovery"]["idea"]["idea_id"]
        == package.discovery.idea.idea_id
    )

    assert (
        data["approval"]["decision"]["status"]
        == "pending"
    )


class FakeDiscoveryEngine:
    def __init__(self, discovery):
        self.discovery = discovery

    def run(self, signal, brand):
        return self.discovery


class FakeApprovalEngine:
    def __init__(self):
        self.called = False

    def generate(self, discovery):
        self.called = True
        return DiscoveryApprovalEngineV0().generate(
            discovery
        )


def test_discovery_workflow_supports_dependency_injection():
    brand = make_brand()
    signal = make_signal()

    discovery = DiscoveryEngineV0().run(
        signal=signal,
        brand=brand,
    )

    fake_approval_engine = FakeApprovalEngine()

    workflow = DiscoveryWorkflowV0(
        discovery_engine=FakeDiscoveryEngine(
            discovery
        ),
        approval_engine=fake_approval_engine,
    )

    package = workflow.run(
        signal=signal,
        brand=brand,
    )

    assert package.discovery is discovery
    assert package.approval is not None
    assert fake_approval_engine.called is True