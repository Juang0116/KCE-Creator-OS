from __future__ import annotations

from datetime import datetime, timezone

from .models import DiscoveryApproval, DiscoveryApprovalDecision


class DiscoveryApprovalDecisionEngineV0:
    """
    Applies a human decision to a pending DiscoveryApproval.

    This engine only changes the approval aggregate. It does not
    start Research, production, publishing, or external I/O.
    """

    ALLOWED_DECISIONS = {"approved", "rejected"}

    def decide(
        self,
        approval: DiscoveryApproval,
        decision: str,
        decided_by: str,
        notes: str = "",
        decided_at: str | None = None,
    ) -> DiscoveryApproval:
        if approval is None:
            raise ValueError("Discovery approval cannot be None.")

        if decision not in self.ALLOWED_DECISIONS:
            raise ValueError(
                "Decision must be 'approved' or 'rejected'."
            )

        if not decided_by:
            raise ValueError("decided_by must not be empty.")

        if approval.decision.status != "pending":
            raise ValueError(
                "Only pending approvals can be decided."
            )

        timestamp = (
            decided_at
            or datetime.now(timezone.utc).isoformat()
        )

        approval.decision = DiscoveryApprovalDecision(
            status=decision,
            decided_by=decided_by,
            decided_at=timestamp,
            notes=notes,
        )

        approval.processing.status = "completed"
        approval.processing.confidence = 1.0
        approval.processing.processed_at = timestamp

        return approval