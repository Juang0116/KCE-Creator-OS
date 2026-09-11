from __future__ import annotations

from src.application import DiscoveryApplicationServiceV0
from src.integrations.supabase import (
    SupabaseDiscoveryPackageRepository,
    SupabaseEventRepository,
    create_supabase_client,
)
from src.orchestration import DiscoveryWorkflowV0
from src.persistence import DiscoveryPackageRepository


def create_discovery_application() -> DiscoveryApplicationServiceV0:
    """
    Build the production Discovery application.

    Composition root for the Discovery vertical slice.

    Infrastructure dependencies are assembled here so that
    application and orchestration layers remain independent
    from concrete Supabase implementations.
    """

    client = create_supabase_client()

    event_repository = SupabaseEventRepository(
        client
    )

    package_repository = DiscoveryPackageRepository(
        SupabaseDiscoveryPackageRepository(client)
    )

    workflow = DiscoveryWorkflowV0(
        event_repository=event_repository
    )

    return DiscoveryApplicationServiceV0(
        workflow=workflow,
        package_repository=package_repository,
    )