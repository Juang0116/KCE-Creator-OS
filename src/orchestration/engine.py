from uuid import uuid4

from src.discovery import DiscoveryEngineV0
from src.discovery_approval import DiscoveryApprovalEngineV0
from src.events import Event, EventRepository

from .models import DiscoveryPackage


class DiscoveryWorkflowV0:
    """
    First operational Discovery workflow.

    Orchestrates:

        RadarSignal
            -> Discovery
            -> ContentIdea
            -> Human Approval Request

    The workflow also records operational events through an injected
    EventRepository.

    This workflow does not approve content,
    publish content, or communicate with external services.
    """

    def __init__(
        self,
        discovery_engine=None,
        approval_engine=None,
        event_repository=None,
    ):
        self.discovery_engine = (
            discovery_engine
            or DiscoveryEngineV0()
        )

        self.approval_engine = (
            approval_engine
            or DiscoveryApprovalEngineV0()
        )

        self.event_repository = (
            event_repository
            or EventRepository()
        )

    def _record_event(
        self,
        event_type: str,
        entity_type: str,
        entity_id: str,
        payload: dict,
    ) -> Event:
        event = Event.create(
            event_id=f"event_{uuid4().hex[:12]}",
            event_type=event_type,
            entity_type=entity_type,
            entity_id=entity_id,
            payload=payload,
        )

        return self.event_repository.save(event)

    def run(
        self,
        signal,
        brand: dict,
    ) -> DiscoveryPackage:

        discovery = self.discovery_engine.run(
            signal=signal,
            brand=brand,
        )

        base_payload = {
            "discovery_id": discovery.discovery_id,
            "signal_id": signal.signal_id,
            "opportunity_id": (
                discovery.opportunity.opportunity_id
                if discovery.opportunity is not None
                else ""
            ),
            "idea_id": (
                discovery.idea.idea_id
                if discovery.idea is not None
                else ""
            ),
        }

        if discovery.idea is None:
            self._record_event(
                event_type="discovery.filtered",
                entity_type="discovery",
                entity_id=discovery.discovery_id,
                payload=base_payload,
            )

            return DiscoveryPackage(
                discovery=discovery,
                approval=None,
            )

        self._record_event(
            event_type="discovery.created",
            entity_type="discovery",
            entity_id=discovery.discovery_id,
            payload=base_payload,
        )

        approval = self.approval_engine.generate(
            discovery
        )

        self._record_event(
            event_type="discovery_approval.requested",
            entity_type="discovery_approval",
            entity_id=approval.approval_id,
            payload={
                **base_payload,
                "approval_id": approval.approval_id,
            },
        )

        return DiscoveryPackage(
            discovery=discovery,
            approval=approval,
        )