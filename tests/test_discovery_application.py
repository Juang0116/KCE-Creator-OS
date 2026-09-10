from src.orchestration import DiscoveryWorkflowV0
from src.persistence import (
    DiscoveryPackageRepository,
    MemoryRepository,
)
from src.application import DiscoveryApplicationServiceV0

from tests.test_discovery import (
    make_brand,
    make_signal,
)


def make_service():
    workflow = DiscoveryWorkflowV0()

    memory_repository = MemoryRepository()

    package_repository = DiscoveryPackageRepository(
        repository=memory_repository
    )

    service = DiscoveryApplicationServiceV0(
        workflow=workflow,
        package_repository=package_repository,
    )

    return service, package_repository


def test_application_service_returns_discovery_package():
    service, _ = make_service()

    package = service.run(
        signal=make_signal(),
        brand=make_brand(),
    )

    assert package.discovery.discovery_id
    assert package.discovery.signal.signal_id
    assert package.discovery.opportunity.opportunity_id
    assert package.discovery.idea is not None
    assert package.approval is not None


def test_application_service_persists_discovery_package():
    service, repository = make_service()

    package = service.run(
        signal=make_signal(),
        brand=make_brand(),
    )

    discovery_id = package.discovery.discovery_id

    assert repository.exists(
        discovery_id
    )

    stored = repository.get(
        discovery_id
    )

    assert stored is package


def test_application_service_returns_same_package_instance_as_repository():
    service, repository = make_service()

    package = service.run(
        signal=make_signal(),
        brand=make_brand(),
    )

    stored = repository.get(
        package.discovery.discovery_id
    )

    assert stored is package


def test_application_service_persists_filtered_discovery():
    service, repository = make_service()

    signal = make_signal()

    package = service.run(
        signal=signal,
        brand={
            "brand_id": "unrelated_brand",
            "name": "Unrelated Brand",
            "mission": "Something unrelated",
            "vision": "Something unrelated",
            "values": [],
            "content_pillars": [],
            "topics": [],
        },
    )

    assert package.discovery.idea is None
    assert package.approval is None

    assert repository.exists(
        package.discovery.discovery_id
    )


def test_application_service_uses_injected_workflow():
    class FakeWorkflow:
        def __init__(self, package):
            self.package = package
            self.called = False

        def run(self, signal, brand):
            self.called = True
            return self.package

    real_workflow = DiscoveryWorkflowV0()

    package = real_workflow.run(
        signal=make_signal(),
        brand=make_brand(),
    )

    fake_workflow = FakeWorkflow(package)

    memory_repository = MemoryRepository()

    package_repository = DiscoveryPackageRepository(
        repository=memory_repository
    )

    service = DiscoveryApplicationServiceV0(
        workflow=fake_workflow,
        package_repository=package_repository,
    )

    result = service.run(
        signal=make_signal(),
        brand=make_brand(),
    )

    assert fake_workflow.called is True
    assert result is package

    assert repository_contains_package(
        package_repository,
        package.discovery.discovery_id,
    )


def repository_contains_package(
    repository,
    discovery_id,
):
    return repository.exists(
        discovery_id
    )