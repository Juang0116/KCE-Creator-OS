from src.application import (
    DiscoveryApplicationServiceV0,
    DiscoveryApprovalApplicationServiceV0,
    DiscoveryFacadeV0,
    DiscoveryQueryServiceV0,
)
from src.discovery_approval import (
    DiscoveryApprovalDecisionWorkflowV0,
)
from src.events import EventRepository
from src.persistence import (
    DiscoveryPackageRepository,
    MemoryRepository,
)
from src.orchestration import DiscoveryWorkflowV0

from tests.test_discovery import (
    make_brand,
    make_signal,
)


def make_facade():
    workflow = DiscoveryWorkflowV0()

    memory_repository = MemoryRepository()

    package_repository = DiscoveryPackageRepository(
        repository=memory_repository
    )

    application_service = DiscoveryApplicationServiceV0(
        workflow=workflow,
        package_repository=package_repository,
    )

    event_repository = EventRepository()

    decision_workflow = DiscoveryApprovalDecisionWorkflowV0(
        event_repository=event_repository,
    )

    approval_service = DiscoveryApprovalApplicationServiceV0(
        decision_workflow=decision_workflow,
        package_repository=package_repository,
    )

    query_service = DiscoveryQueryServiceV0(
        package_repository=package_repository,
    )

    facade = DiscoveryFacadeV0(
        application_service=application_service,
        approval_service=approval_service,
        query_service=query_service,
    )

    return facade


def test_facade_run_returns_discovery_package():
    facade = make_facade()

    package = facade.run(
        signal=make_signal(),
        brand=make_brand(),
    )

    assert package.discovery is not None
    assert package.discovery.idea is not None
    assert package.approval is not None


def test_facade_decide_approved_updates_package():
    facade = make_facade()

    package = facade.run(
        signal=make_signal(),
        brand=make_brand(),
    )

    result = facade.decide(
        discovery_id=package.discovery.discovery_id,
        decision="approved",
        decided_by="juancho",
        notes="Approved for research.",
    )

    assert result is package
    assert result.approval is not None
    assert result.approval.decision.status == "approved"
    assert result.approval.decision.decided_by == "juancho"
    assert result.approval.decision.notes == (
        "Approved for research."
    )


def test_facade_decide_rejected_updates_package():
    facade = make_facade()

    package = facade.run(
        signal=make_signal(),
        brand=make_brand(),
    )

    result = facade.decide(
        discovery_id=package.discovery.discovery_id,
        decision="rejected",
        decided_by="juancho",
        notes="Rejected for current strategy.",
    )

    assert result is package
    assert result.approval is not None
    assert result.approval.decision.status == "rejected"
    assert result.approval.decision.decided_by == "juancho"
    assert result.approval.decision.notes == (
        "Rejected for current strategy."
    )


def test_facade_get_returns_persisted_package():
    facade = make_facade()

    package = facade.run(
        signal=make_signal(),
        brand=make_brand(),
    )

    result = facade.get(
        package.discovery.discovery_id
    )

    assert result is package


def test_facade_get_returns_none_for_missing_package():
    facade = make_facade()

    result = facade.get(
        "discovery_missing"
    )

    assert result is None


def test_facade_exists_returns_true_for_existing_package():
    facade = make_facade()

    package = facade.run(
        signal=make_signal(),
        brand=make_brand(),
    )

    assert (
        facade.exists(
            package.discovery.discovery_id
        )
        is True
    )


def test_facade_exists_returns_false_for_missing_package():
    facade = make_facade()

    assert (
        facade.exists(
            "discovery_missing"
        )
        is False
    )


def test_facade_list_all_returns_persisted_packages():
    facade = make_facade()

    package_1 = facade.run(
        signal=make_signal(),
        brand=make_brand(),
    )

    package_2 = facade.run(
        signal=make_signal(),
        brand=make_brand(),
    )

    packages = facade.list_all()

    assert len(packages) == 2
    assert package_1 in packages
    assert package_2 in packages