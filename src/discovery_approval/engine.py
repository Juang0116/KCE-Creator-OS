from datetime import datetime, timezone
from uuid import uuid4

from src.discovery import DiscoveryResult

from .models import (
    DiscoveryApproval,
    DiscoveryApprovalDecision,
    DiscoveryApprovalProcessing,
    DiscoveryApprovalSource,
    DiscoveryApprovalTarget,
)


class DiscoveryApprovalEngineV0:
    """
    Human approval gate for Discovery V0.

    Creates an explicit pending approval request
    for a generated ContentIdea.

    This engine never approves content automatically.
    """

    def generate(
        self,
        discovery: DiscoveryResult,
    ) -> DiscoveryApproval:

        if discovery.idea is None:
            raise ValueError(
                "Cannot create discovery approval "
                "without a ContentIdea."
            )

        processed_at = (
            datetime.now(
                timezone.utc
            ).isoformat()
        )

        source = DiscoveryApprovalSource(
            discovery_id=discovery.discovery_id,
            idea_id=discovery.idea.idea_id,
            opportunity_id=(
                discovery.opportunity.opportunity_id
            ),
            signal_id=discovery.signal.signal_id,
        )

        target = DiscoveryApprovalTarget(
            brand_id=discovery.idea.brand_id,
            channel=discovery.idea.channel,
            platform=discovery.idea.platform,
        )

        decision = DiscoveryApprovalDecision(
            status="pending",
            decided_by=None,
            decided_at=None,
            notes="",
        )

        processing = DiscoveryApprovalProcessing(
            status="pending",
            confidence=1.0,
            processed_at=processed_at,
        )

        return DiscoveryApproval(
            schema_version="1.0",
            approval_id=(
                f"discovery_approval_"
                f"{uuid4().hex[:12]}"
            ),
            created_at=processed_at,
            approval_version="1",
            source=source,
            target=target,
            decision=decision,
            processing=processing,
        )