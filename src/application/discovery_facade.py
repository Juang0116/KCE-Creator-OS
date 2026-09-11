from __future__ import annotations

from src.orchestration import DiscoveryPackage

from .discovery import DiscoveryApplicationServiceV0
from .discovery_query import DiscoveryQueryServiceV0


class DiscoveryFacadeV0:
    """
    Unified application entry point for the Discovery vertical slice.

    Commands:
        run()

    Queries:
        get()
        exists()
        list_all()

    The facade coordinates existing application services.
    It does not contain Discovery domain logic.
    """

    def __init__(
        self,
        application_service: DiscoveryApplicationServiceV0,
        query_service: DiscoveryQueryServiceV0,
    ) -> None:
        self.application_service = application_service
        self.query_service = query_service

    def run(
        self,
        signal,
        brand: dict,
    ) -> DiscoveryPackage:
        return self.application_service.run(
            signal=signal,
            brand=brand,
        )

    def get(
        self,
        discovery_id: str,
    ) -> DiscoveryPackage | None:
        return self.query_service.get(
            discovery_id=discovery_id,
        )

    def exists(
        self,
        discovery_id: str,
    ) -> bool:
        return self.query_service.exists(
            discovery_id=discovery_id,
        )

    def list_all(self) -> list[DiscoveryPackage]:
        return self.query_service.list_all()