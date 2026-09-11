from __future__ import annotations

from src.orchestration import DiscoveryPackage
from src.persistence import DiscoveryPackageRepository


class DiscoveryQueryServiceV0:
    """
    Application service for reading persisted DiscoveryPackage objects.

    Responsibilities:

        1. Retrieve a DiscoveryPackage by discovery_id.
        2. Check whether a DiscoveryPackage exists.
        3. List all persisted DiscoveryPackages.

    The service does not contain Discovery domain logic.

    Persistence is injected so the application layer remains
    independent from the concrete storage implementation.
    """

    def __init__(
        self,
        package_repository: DiscoveryPackageRepository,
    ) -> None:
        self.package_repository = package_repository

    def get(
        self,
        discovery_id: str,
    ) -> DiscoveryPackage | None:
        """
        Retrieve a persisted DiscoveryPackage by discovery_id.
        """

        return self.package_repository.get(
            discovery_id
        )

    def exists(
        self,
        discovery_id: str,
    ) -> bool:
        """
        Check whether a DiscoveryPackage exists.
        """

        return self.package_repository.exists(
            discovery_id
        )

    def list_all(
        self,
    ) -> list[DiscoveryPackage]:
        """
        Return all persisted DiscoveryPackages.
        """

        return self.package_repository.list_all()