from __future__ import annotations

from uuid import uuid4

from src.events import Event, EventRepository

from .decision import DiscoveryApprovalDecisionEngineV0


class DiscoveryApprovalDecisionWorkflowV0:
    """
    Applies a human Discovery Approval decision and records
    the corresponding operational event.
    """

    def __init__(
        self,
        decision_engine=None,
        event_repository=None,
    ):
        self.decision_engine = (
            decision_engine
            or DiscoveryApprovalDecisionEngineV0()
        )
        self.event_repository = (
            event_repository
            or EventRepository()
        )

    def _record_event(self, event_type: str, approval) -> Event:
        event = Event.create(
            event_id=f"event_{uuid4().hex[:12]}",
            event_type=event_type,
            entity_type="discovery_approval",
            entity_id=approval.approval_id,
            payload={
                "approval_id": approval.approval_id,
                "discovery_id": approval.source.discovery_id,
                "idea_id": approval.source.idea_id,
                "opportunity_id": approval.source.opportunity_id,
                "signal_id": approval.source.signal_id,
                "decision": approval.decision.status,
                "decided_by": approval.decision.decided_by,
                "decided_at": approval.decision.decided_at,
            },
        )

        return self.event_repository.save(event)

    def decide(
        self,
        approval,
        decision: str,
        decided_by: str,
        notes: str = "",
        decided_at: str | None = None,
    ):
        result = self.decision_engine.decide(
            approval=approval,
            decision=decision,
            decided_by=decided_by,
            notes=notes,
            decided_at=decided_at,
        )

        event_type = (
            "discovery_approval.approved"
            if decision == "approved"
            else "discovery_approval.rejected"
        )

        self._record_event(event_type, result)

        return result