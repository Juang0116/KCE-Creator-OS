from src.application.discovery_query import (
    DiscoveryQueryServiceV0,
)
from src.persistence import (
    DiscoveryPackageRepository,
    MemoryRepository,
)

from tests.test_discovery import (
    make_brand,
    make_signal,
)
from src.orchestration import DiscoveryWorkflowV0


def make_package():
    workflow = DiscoveryWorkflowV0()

    return workflow.run(
        signal=make_signal(),
        brand=make_brand(),
    )


def make_query_service():
    memory_repository = MemoryRepository()

    package_repository = DiscoveryPackageRepository(
        repository=memory_repository
    )

    return DiscoveryQueryServiceV0(
        package_repository=package_repository
    )


def test_query_get_returns_persisted_package():
    package = make_package()
    query_service = make_query_service()

    query_service.package_repository.save(package)

    result = query_service.get(
        package.discovery.discovery_id
    )

    assert result is package


def test_query_get_returns_none_for_missing_package():
    query_service = make_query_service()

    result = query_service.get(
        "discovery_missing"
    )

    assert result is None


def test_query_exists_returns_true_for_existing_package():
    package = make_package()
    query_service = make_query_service()

    query_service.package_repository.save(package)

    assert query_service.exists(
        package.discovery.discovery_id
    ) is True


def test_query_exists_returns_false_for_missing_package():
    query_service = make_query_service()

    assert query_service.exists(
        "discovery_missing"
    ) is False


def test_query_list_all_returns_all_packages():
    package_1 = make_package()
    package_2 = make_package()

    package_2.discovery.discovery_id = (
        "discovery_002"
    )

    query_service = make_query_service()

    query_service.package_repository.save(
        package_1
    )
    query_service.package_repository.save(
        package_2
    )

    packages = query_service.list_all()

    assert len(packages) == 2
    assert package_1 in packages
    assert package_2 in packages