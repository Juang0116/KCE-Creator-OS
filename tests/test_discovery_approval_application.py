from __future__ import annotations

from dataclasses import dataclass

import pytest

from src.application.discovery_approval import (
    DiscoveryApprovalApplicationServiceV0,
)
from src.discovery_approval import (
    DiscoveryApprovalDecisionWorkflowV0,
)
from src.orchestration import DiscoveryPackage


class FakePackageRepository:
    """Minimal repository double for the application-service tests."""

    def __init__(self, package=None):
        self.package = package
        self.saved_packages = []

    def get(self, discovery_id):
        if self.package is None:
            return None

        if self.package.discovery.discovery_id != discovery_id:
            return None

        return self.package

    def save(self, package):
        self.saved_packages.append(package)
        self.package = package
        return package


class FakeEventRepository:
    """Minimal event repository double."""

    def __init__(self):
        self.events = []

    def save(self, event):
        self.events.append(event)
        return event

    def get(self, event_id):
        for event in self.events:
            if event.event_id == event_id:
                return event
        return None

    def list_all(self):
        return list(self.events)


@dataclass
class FakeDiscovery:
    discovery_id: str


@dataclass
class FakeApproval:
    approval_id: str


def build_package(approval=True):
    discovery = FakeDiscovery(discovery_id="discovery_test_001")

    package = DiscoveryPackage(
        discovery=discovery,
        approval=approval,
    )

    return package


def build_real_package():
    """
    Build a package using the real DiscoveryApproval aggregate.

    This keeps the application-service tests focused on the application
    boundary while using the actual approval decision workflow.
    """
    from src.discovery_approval import (
        DiscoveryApproval,
        DiscoveryApprovalDecision,
        DiscoveryApprovalProcessing,
        DiscoveryApprovalSource,
        DiscoveryApprovalTarget,
    )

    discovery = FakeDiscovery(discovery_id="discovery_test_001")

    approval = DiscoveryApproval(
        schema_version="1.0",
        approval_id="discovery_approval_test_001",
        created_at="2026-01-01T00:00:00+00:00",
        approval_version="1",
        source=DiscoveryApprovalSource(
            discovery_id="discovery_test_001",
            idea_id="idea_test_001",
            opportunity_id="opportunity_test_001",
            signal_id="signal_test_001",
        ),
        target=DiscoveryApprovalTarget(
            brand_id="brand_test",
            channel="Test Channel",
            platform="youtube",
        ),
        decision=DiscoveryApprovalDecision(
            status="pending",
            decided_by=None,
            decided_at=None,
            notes="",
        ),
        processing=DiscoveryApprovalProcessing(
            status="pending",
            confidence=1.0,
            processed_at="2026-01-01T00:00:00+00:00",
        ),
    )

    return DiscoveryPackage(
        discovery=discovery,
        approval=approval,
    )


def build_service(package):
    repository = FakePackageRepository(package)

    event_repository = FakeEventRepository()

    decision_workflow = DiscoveryApprovalDecisionWorkflowV0(
        event_repository=event_repository,
    )

    service = DiscoveryApprovalApplicationServiceV0(
        decision_workflow=decision_workflow,
        package_repository=repository,
    )

    return service, repository, event_repository


def test_approve_loads_decides_and_persists_package():
    package = build_real_package()

    service, repository, event_repository = build_service(package)

    result = service.decide(
        discovery_id="discovery_test_001",
        decision="approved",
        decided_by="juancho",
        notes="Approved for research.",
    )

    assert result is package
    assert result.approval is not None
    assert result.approval.decision.status == "approved"
    assert result.approval.decision.decided_by == "juancho"
    assert result.approval.decision.notes == "Approved for research."

    assert repository.saved_packages == [package]
    assert repository.get("discovery_test_001") is package

    assert len(event_repository.events) == 1
    assert event_repository.events[0].event_type == "discovery_approval.approved"


def test_reject_loads_decides_and_persists_package():
    package = build_real_package()

    service, repository, event_repository = build_service(package)

    result = service.decide(
        discovery_id="discovery_test_001",
        decision="rejected",
        decided_by="juancho",
        notes="Not aligned with the current content strategy.",
    )

    assert result is package
    assert result.approval is not None
    assert result.approval.decision.status == "rejected"
    assert result.approval.decision.decided_by == "juancho"
    assert (
        result.approval.decision.notes
        == "Not aligned with the current content strategy."
    )

    assert repository.saved_packages == [package]
    assert repository.get("discovery_test_001") is package

    assert len(event_repository.events) == 1
    assert event_repository.events[0].event_type == "discovery_approval.rejected"


def test_missing_discovery_id_is_rejected():
    package = build_real_package()

    service, repository, event_repository = build_service(package)

    with pytest.raises(ValueError, match="discovery_id must not be empty"):
        service.decide(
            discovery_id="",
            decision="approved",
            decided_by="juancho",
        )

    assert repository.saved_packages == []
    assert event_repository.events == []


def test_missing_package_is_rejected():
    service, repository, event_repository = build_service(None)

    with pytest.raises(ValueError, match="DiscoveryPackage was not found"):
        service.decide(
            discovery_id="discovery_does_not_exist",
            decision="approved",
            decided_by="juancho",
        )

    assert repository.saved_packages == []
    assert event_repository.events == []


def test_package_without_approval_is_rejected():
    package = build_package(approval=None)

    service, repository, event_repository = build_service(package)

    with pytest.raises(
        ValueError,
        match="DiscoveryPackage does not contain a DiscoveryApproval",
    ):
        service.decide(
            discovery_id="discovery_test_001",
            decision="approved",
            decided_by="juancho",
        )

    assert repository.saved_packages == []
    assert event_repository.events == []


def test_invalid_decision_is_rejected_and_not_persisted():
    package = build_real_package()

    service, repository, event_repository = build_service(package)

    with pytest.raises(
        ValueError,
        match="Decision must be 'approved' or 'rejected'",
    ):
        service.decide(
            discovery_id="discovery_test_001",
            decision="maybe",
            decided_by="juancho",
        )

    assert package.approval.decision.status == "pending"
    assert repository.saved_packages == []
    assert event_repository.events == []


def test_empty_decided_by_is_rejected_and_not_persisted():
    package = build_real_package()

    service, repository, event_repository = build_service(package)

    with pytest.raises(ValueError, match="decided_by cannot be empty"):
        service.decide(
            discovery_id="discovery_test_001",
            decision="approved",
            decided_by="",
        )

    assert package.approval.decision.status == "pending"
    assert repository.saved_packages == []
    assert event_repository.events == []


def test_decision_with_explicit_timestamp_is_persisted():
    package = build_real_package()

    service, repository, event_repository = build_service(package)

    decided_at = "2026-09-11T23:00:00+00:00"

    result = service.decide(
        discovery_id="discovery_test_001",
        decision="approved",
        decided_by="juancho",
        notes="Explicit timestamp test.",
        decided_at=decided_at,
    )

    assert result.approval.decision.status == "approved"
    assert result.approval.decision.decided_at == decided_at

    assert result.approval.processing.status == "completed"
    assert result.approval.processing.processed_at == decided_at

    assert len(repository.saved_packages) == 1
    assert len(event_repository.events) == 1

    event = event_repository.events[0]
    assert event.event_type == "discovery_approval.approved"
    assert event.entity_type == "discovery_approval"
    assert event.entity_id == result.approval.approval_id