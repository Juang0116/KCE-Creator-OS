from __future__ import annotations

from src.discovery_approval import (
    DiscoveryApprovalDecisionWorkflowV0,
)
from src.orchestration import DiscoveryPackage
from src.persistence import DiscoveryPackageRepository


class DiscoveryApprovalApplicationServiceV0:
    """
    Application service for the Discovery Approval decision use case.

    Responsibilities:

        1. Load an existing DiscoveryPackage.
        2. Apply a human approval decision.
        3. Persist the updated DiscoveryPackage.
        4. Return the updated package.

    The service does not contain approval domain logic.
    That responsibility remains inside
    DiscoveryApprovalDecisionWorkflowV0.

    The service does not execute Research, ContentPipeline,
    publishing, or any other downstream workflow.
    """

    def __init__(
        self,
        decision_workflow: DiscoveryApprovalDecisionWorkflowV0,
        package_repository: DiscoveryPackageRepository,
    ) -> None:
        self.decision_workflow = decision_workflow
        self.package_repository = package_repository

    def decide(
        self,
        discovery_id: str,
        decision: str,
        decided_by: str,
        notes: str = "",
        decided_at: str | None = None,
    ) -> DiscoveryPackage:
        """
        Apply and persist a human decision for a DiscoveryPackage.
        """

        if not discovery_id:
            raise ValueError(
                "discovery_id must not be empty."
            )

        package = self.package_repository.get(
            discovery_id
        )

        if package is None:
            raise ValueError(
                "DiscoveryPackage was not found."
            )

        if package.approval is None:
            raise ValueError(
                "DiscoveryPackage does not contain "
                "a DiscoveryApproval."
            )

        self.decision_workflow.decide(
            approval=package.approval,
            decision=decision,
            decided_by=decided_by,
            notes=notes,
            decided_at=decided_at,
        )

        return self.package_repository.save(
            package
        )