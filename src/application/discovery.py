from __future__ import annotations

from src.orchestration import DiscoveryPackage, DiscoveryWorkflowV0
from src.persistence import DiscoveryPackageRepository


class DiscoveryApplicationServiceV0:
    """
    Application service for the Discovery use case.

    Responsibilities:

        1. Execute the Discovery workflow.
        2. Persist the resulting DiscoveryPackage.
        3. Return the persisted package.

    The service does not contain Discovery domain logic.
    That responsibility remains inside DiscoveryWorkflowV0.

    Persistence is injected so the application layer remains
    independent from the concrete storage implementation.
    """

    def __init__(
        self,
        workflow: DiscoveryWorkflowV0,
        package_repository: DiscoveryPackageRepository,
    ) -> None:
        self.workflow = workflow
        self.package_repository = package_repository

    def run(
        self,
        signal,
        brand: dict,
    ) -> DiscoveryPackage:
        """
        Execute Discovery and persist the resulting package.
        """

        package = self.workflow.run(
            signal=signal,
            brand=brand,
        )

        self.package_repository.save(
            package
        )

        return package