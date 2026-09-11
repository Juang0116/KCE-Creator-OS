from unittest.mock import patch

from src.application import DiscoveryApplicationServiceV0
from src.bootstrap import create_discovery_application
from src.events import EventRepository
from src.persistence import MemoryRepository
from tests.test_discovery import make_brand, make_signal


def test_create_discovery_application_wires_dependencies():
    fake_client = object()

    with patch(
        "src.bootstrap.discovery.create_supabase_client",
        return_value=fake_client,
    ):
        application = create_discovery_application()

    assert isinstance(application, DiscoveryApplicationServiceV0)
    assert application.workflow.event_repository.client is fake_client

    package_repository = application.package_repository.repository
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

    assert package.discovery.signal.signal_id == "sig_discovery_001"
    assert package.discovery.idea.signal_id == "sig_discovery_001"

    assert (
        package.approval.source.discovery_id
        == package.discovery.discovery_id
    )

    assert application.workflow.event_repository is event_repository

    assert (
        application.package_repository.get(
            package.discovery.discovery_id
        )
        is package
    )

    events = event_repository.list_all()

    assert len(events) == 2
    assert {event.event_type for event in events} == {
        "discovery.created",
        "discovery_approval.requested",
    }