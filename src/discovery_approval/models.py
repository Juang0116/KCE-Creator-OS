from dataclasses import dataclass, field
from typing import Optional

from src.discovery import DiscoveryResult


@dataclass
class DiscoveryApprovalSource:
    discovery_id: str
    idea_id: str
    opportunity_id: str
    signal_id: str

    def to_dict(self) -> dict:
        return {
            "discovery_id": self.discovery_id,
            "idea_id": self.idea_id,
            "opportunity_id": self.opportunity_id,
            "signal_id": self.signal_id,
        }


@dataclass
class DiscoveryApprovalTarget:
    brand_id: str
    channel: str
    platform: str

    def to_dict(self) -> dict:
        return {
            "brand_id": self.brand_id,
            "channel": self.channel,
            "platform": self.platform,
        }


@dataclass
class DiscoveryApprovalDecision:
    status: str = "pending"
    decided_by: Optional[str] = None
    decided_at: Optional[str] = None
    notes: str = ""

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "decided_by": self.decided_by,
            "decided_at": self.decided_at,
            "notes": self.notes,
        }


@dataclass
class DiscoveryApprovalProcessing:
    status: str = "pending"
    confidence: float = 0.0
    processed_at: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "confidence": self.confidence,
            "processed_at": self.processed_at,
        }


@dataclass
class DiscoveryApproval:
    schema_version: str
    approval_id: str
    created_at: str
    approval_version: str

    source: DiscoveryApprovalSource
    target: DiscoveryApprovalTarget

    decision: DiscoveryApprovalDecision = field(
        default_factory=DiscoveryApprovalDecision
    )

    processing: DiscoveryApprovalProcessing = field(
        default_factory=DiscoveryApprovalProcessing
    )

    def to_dict(self) -> dict:
        return {
            "schema_version": self.schema_version,
            "approval_id": self.approval_id,
            "created_at": self.created_at,
            "approval_version": self.approval_version,
            "source": self.source.to_dict(),
            "target": self.target.to_dict(),
            "decision": self.decision.to_dict(),
            "processing": self.processing.to_dict(),
        }