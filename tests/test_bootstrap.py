from unittest.mock import patch

from src.application import DiscoveryApplicationServiceV0
from src.bootstrap import create_discovery_application


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