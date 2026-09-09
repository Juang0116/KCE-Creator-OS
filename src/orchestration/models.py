from dataclasses import dataclass
from typing import Optional

from src.discovery import DiscoveryResult
from src.discovery_approval import DiscoveryApproval


@dataclass
class DiscoveryPackage:
    discovery: DiscoveryResult
    approval: Optional[DiscoveryApproval] = None

    def to_dict(self) -> dict:
        return {
            "discovery": self.discovery.to_dict(),
            "approval": (
                self.approval.to_dict()
                if self.approval is not None
                else None
            ),
        }