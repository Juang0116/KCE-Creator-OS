from src.discovery import DiscoveryEngineV0
from src.discovery_approval import DiscoveryApprovalEngineV0

from .models import DiscoveryPackage


class DiscoveryWorkflowV0:
    """
    First operational Discovery workflow.

    Orchestrates:

        RadarSignal
            -> Discovery
            -> ContentIdea
            -> Human Approval Request

    This workflow does not approve content,
    publish content, or communicate with external services.
    """

    def __init__(
        self,
        discovery_engine=None,
        approval_engine=None,
    ):
        self.discovery_engine = (
            discovery_engine
            or DiscoveryEngineV0()
        )

        self.approval_engine = (
            approval_engine
            or DiscoveryApprovalEngineV0()
        )

    def run(
        self,
        signal,
        brand: dict,
    ) -> DiscoveryPackage:

        discovery = self.discovery_engine.run(
            signal=signal,
            brand=brand,
        )

        if discovery.idea is None:
            return DiscoveryPackage(
                discovery=discovery,
                approval=None,
            )

        approval = self.approval_engine.generate(
            discovery
        )

        return DiscoveryPackage(
            discovery=discovery,
            approval=approval,
        )