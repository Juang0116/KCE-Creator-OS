from unittest.mock import patch

from src.application import (
    DiscoveryApprovalApplicationServiceV0,
    DiscoveryFacadeV0,
    DiscoveryApplicationServiceV0,
    DiscoveryQueryServiceV0,
)
from src.bootstrap import (
    create_discovery,
    create_discovery_application,
    create_discovery_query,
)
from src.events import EventRepository
from src.persistence import (
    DiscoveryPackageRepository,
    MemoryRepository,
)

from tests.test_discovery import (
    make_brand,
    make_signal,
)


def test_create_discovery_application_wires_dependencies():
    fake_client = object()

    with patch(
        "src.bootstrap.discovery.create_supabase_client",
        return_value=fake_client,
    ):
        application = create_discovery_application()

    assert isinstance(
        application,
        DiscoveryApplicationServiceV0,
    )

    assert (
        application.workflow.event_repository.client
        is fake_client
    )

    package_repository = (
        application.package_repository.repository
    )

    assert package_repository.client is fake_client


def test_create_discovery_application_runs_discovery_circuit():
    fake_client = object()

    event_repository = EventRepository()
    package_store = MemoryRepository()

    with (
        patch(
            "src.bootstrap.discovery.create_supabase_client",
            return_value=fake_client,
        ),
        patch(
            "src.bootstrap.discovery.SupabaseEventRepository",
            return_value=event_repository,
        ),
        patch(
            "src.bootstrap.discovery.SupabaseDiscoveryPackageRepository",
            return_value=package_store,
        ),
    ):
        application = create_discovery_application()

        package = application.run(
            signal=make_signal(),
            brand=make_brand(),
        )

    assert package.discovery is not None
    assert package.discovery.idea is not None
    assert package.approval is not None

    assert (
        package.discovery.signal.signal_id
        == "sig_discovery_001"
    )

    assert (
        package.discovery.idea.signal_id
        == "sig_discovery_001"
    )

    assert (
        package.approval.source.discovery_id
        == package.discovery.discovery_id
    )

    assert (
        application.workflow.event_repository
        is event_repository
    )

    assert (
        application.package_repository.get(
            package.discovery.discovery_id
        )
        is package
    )

    events = event_repository.list_all()

    assert len(events) == 2

    assert {
        event.event_type
        for event in events
    } == {
        "discovery.created",
        "discovery_approval.requested",
    }


def test_create_discovery_query_wires_dependencies():
    fake_client = object()

    with patch(
        "src.bootstrap.discovery.create_supabase_client",
        return_value=fake_client,
    ):
        query_service = create_discovery_query()

    assert isinstance(
        query_service,
        DiscoveryQueryServiceV0,
    )

    assert isinstance(
        query_service.package_repository,
        DiscoveryPackageRepository,
    )

    repository = (
        query_service.package_repository.repository
    )

    assert repository.client is fake_client


def test_create_discovery_query_reads_from_repository():
    fake_client = object()

    package_store = MemoryRepository()

    with (
        patch(
            "src.bootstrap.discovery.create_supabase_client",
            return_value=fake_client,
        ),
        patch(
            "src.bootstrap.discovery.SupabaseDiscoveryPackageRepository",
            return_value=package_store,
        ),
    ):
        query_service = create_discovery_query()

        package_repository = (
            query_service.package_repository
        )

        from src.orchestration import DiscoveryWorkflowV0

        workflow = DiscoveryWorkflowV0()

        package = workflow.run(
            signal=make_signal(),
            brand=make_brand(),
        )

        package_repository.save(package)

        result = query_service.get(
            package.discovery.discovery_id
        )

    assert result is package


def test_create_discovery_wires_facade():
    fake_client = object()

    with patch(
        "src.bootstrap.discovery.create_supabase_client",
        return_value=fake_client,
    ):
        discovery = create_discovery()

    assert isinstance(
        discovery,
        DiscoveryFacadeV0,
    )

    assert isinstance(
        discovery.application_service,
        DiscoveryApplicationServiceV0,
    )

    assert isinstance(
        discovery.approval_service,
        DiscoveryApprovalApplicationServiceV0,
    )

    assert isinstance(
        discovery.query_service,
        DiscoveryQueryServiceV0,
    )