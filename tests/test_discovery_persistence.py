import pytest

from src.orchestration import DiscoveryWorkflowV0
from src.persistence import (
    DiscoveryPackageRepository,
    MemoryRepository,
)

from tests.test_discovery import (
    make_brand,
    make_signal,
)


def make_package():
    workflow = DiscoveryWorkflowV0()

    return workflow.run(
        signal=make_signal(),
        brand=make_brand(),
    )


def make_repository():
    memory_repository = (
        MemoryRepository()
    )

    return DiscoveryPackageRepository(
        repository=memory_repository
    )


def test_discovery_repository_saves_package():
    package = make_package()

    repository = make_repository()

    result = repository.save(
        package
    )

    assert result is package

    assert repository.exists(
        package.discovery.discovery_id
    )


def test_discovery_repository_gets_package():
    package = make_package()

    repository = make_repository()

    repository.save(package)

    result = repository.get(
        package.discovery.discovery_id
    )

    assert result is package


def test_discovery_repository_returns_none_for_missing_package():
    repository = make_repository()

    result = repository.get(
        "discovery_missing"
    )

    assert result is None


def test_discovery_repository_preserves_lineage():
    package = make_package()

    repository = make_repository()

    repository.save(package)

    result = repository.get(
        package.discovery.discovery_id
    )

    assert result is package

    assert (
        result.discovery.discovery_id
        == package.discovery.discovery_id
    )

    assert (
        result.discovery.signal.signal_id
        == package.discovery.signal.signal_id
    )

    assert (
        result.discovery.opportunity.opportunity_id
        == package.discovery.opportunity.opportunity_id
    )

    assert (
        result.discovery.idea.idea_id
        == package.discovery.idea.idea_id
    )

    assert (
        result.approval.approval_id
        == package.approval.approval_id
    )


def test_discovery_repository_replaces_package_with_same_id():
    package = make_package()

    repository = make_repository()

    repository.save(package)

    replacement = make_package()

    replacement.discovery.discovery_id = (
        package.discovery.discovery_id
    )

    repository.save(replacement)

    result = repository.get(
        package.discovery.discovery_id
    )

    assert result is replacement
    assert len(repository.list_all()) == 1


def test_discovery_repository_lists_packages():
    package_1 = make_package()
    package_2 = make_package()

    package_2.discovery.discovery_id = (
        "discovery_002"
    )

    repository = make_repository()

    repository.save(package_1)
    repository.save(package_2)

    packages = repository.list_all()

    assert len(packages) == 2
    assert package_1 in packages
    assert package_2 in packages


def test_discovery_repository_deletes_package():
    package = make_package()

    repository = make_repository()

    repository.save(package)

    result = repository.delete(
        package.discovery.discovery_id
    )

    assert result is True

    assert not repository.exists(
        package.discovery.discovery_id
    )

    assert repository.get(
        package.discovery.discovery_id
    ) is None


def test_discovery_repository_delete_missing_returns_false():
    repository = make_repository()

    result = repository.delete(
        "discovery_missing"
    )

    assert result is False


def test_discovery_repository_rejects_missing_discovery_id():
    package = make_package()

    package.discovery.discovery_id = ""

    repository = make_repository()

    with pytest.raises(ValueError):
        repository.save(package)


def test_discovery_repository_can_handle_filtered_package():
    package = make_package()

    package.discovery.idea = None
    package.approval = None

    repository = make_repository()

    result = repository.save(package)

    assert result is package

    assert repository.exists(
        package.discovery.discovery_id
    )