from __future__ import annotations

from src.orchestration import DiscoveryPackage

from .protocols import Repository


class DiscoveryPackageRepository:
    """
    Typed repository for DiscoveryPackage objects.

    The application works with DiscoveryPackage directly,
    while the underlying persistence implementation remains
    replaceable.
    """

    def __init__(
        self,
        repository: Repository[DiscoveryPackage],
    ) -> None:
        self.repository = repository

    def save(
        self,
        package: DiscoveryPackage,
    ) -> DiscoveryPackage:
        """
        Persist a DiscoveryPackage using its discovery_id
        as the stable storage key.
        """

        discovery_id = (
            package.discovery.discovery_id
        )

        if not discovery_id:
            raise ValueError(
                "DiscoveryPackage must contain "
                "a valid discovery_id."
            )

        return self.repository.save(
            key=discovery_id,
            value=package,
        )

    def get(
        self,
        discovery_id: str,
    ) -> DiscoveryPackage | None:
        """
        Retrieve a DiscoveryPackage by discovery_id.
        """

        return self.repository.get(
            discovery_id
        )

    def exists(
        self,
        discovery_id: str,
    ) -> bool:
        """
        Check whether a DiscoveryPackage exists.
        """

        return self.repository.exists(
            discovery_id
        )

    def delete(
        self,
        discovery_id: str,
    ) -> bool:
        """
        Delete a DiscoveryPackage.
        """

        return self.repository.delete(
            discovery_id
        )

    def list_all(
        self,
    ) -> list[DiscoveryPackage]:
        """
        Return all persisted DiscoveryPackages.
        """

        return self.repository.list_all()