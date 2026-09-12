from src.application import (
    DiscoveryApplicationServiceV0,
    DiscoveryApprovalApplicationServiceV0,
    DiscoveryFacadeV0,
    DiscoveryQueryServiceV0,
)
from src.integrations.supabase import (
    SupabaseDiscoveryPackageRepository,
    SupabaseEventRepository,
    create_supabase_client,
)
from src.discovery_approval import (
    DiscoveryApprovalDecisionWorkflowV0,
)
from src.orchestration import DiscoveryWorkflowV0
from src.persistence import DiscoveryPackageRepository


def create_discovery_application() -> DiscoveryApplicationServiceV0:
    client = create_supabase_client()

    event_repository = SupabaseEventRepository(client)

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


def create_discovery_approval_application() -> (
    DiscoveryApprovalApplicationServiceV0
):
    client = create_supabase_client()

    event_repository = SupabaseEventRepository(client)

    package_repository = DiscoveryPackageRepository(
        SupabaseDiscoveryPackageRepository(client)
    )

    decision_workflow = DiscoveryApprovalDecisionWorkflowV0(
        event_repository=event_repository,
    )

    return DiscoveryApprovalApplicationServiceV0(
        decision_workflow=decision_workflow,
        package_repository=package_repository,
    )


def create_discovery_query() -> DiscoveryQueryServiceV0:
    client = create_supabase_client()

    package_repository = DiscoveryPackageRepository(
        SupabaseDiscoveryPackageRepository(client)
    )

    return DiscoveryQueryServiceV0(
        package_repository=package_repository
    )


def create_discovery() -> DiscoveryFacadeV0:
    client = create_supabase_client()

    event_repository = SupabaseEventRepository(client)

    package_repository = DiscoveryPackageRepository(
        SupabaseDiscoveryPackageRepository(client)
    )

    workflow = DiscoveryWorkflowV0(
        event_repository=event_repository
    )

    application_service = DiscoveryApplicationServiceV0(
        workflow=workflow,
        package_repository=package_repository,
    )

    decision_workflow = DiscoveryApprovalDecisionWorkflowV0(
        event_repository=event_repository,
    )

    approval_service = DiscoveryApprovalApplicationServiceV0(
        decision_workflow=decision_workflow,
        package_repository=package_repository,
    )

    query_service = DiscoveryQueryServiceV0(
        package_repository=package_repository,
    )

    return DiscoveryFacadeV0(
        application_service=application_service,
        approval_service=approval_service,
        query_service=query_service,
    )