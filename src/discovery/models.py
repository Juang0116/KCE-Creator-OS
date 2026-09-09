from dataclasses import dataclass, field
from typing import Optional

from src.brand_brain import BrandEvaluation
from src.content.ideas import ContentIdea
from src.opportunity import Opportunity
from src.radar import RadarSignal


@dataclass
class DiscoveryProcessing:
    status: str = "draft"
    confidence: float = 0.0
    processed_at: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "confidence": self.confidence,
            "processed_at": self.processed_at,
        }


@dataclass
class DiscoveryResult:
    discovery_id: str
    created_at: str
    discovery_version: str
    signal: RadarSignal
    brand_evaluation: BrandEvaluation
    opportunity: Opportunity
    idea: Optional[ContentIdea] = None
    processing: DiscoveryProcessing = field(
        default_factory=DiscoveryProcessing
    )

    def to_dict(self) -> dict:
        return {
            "schema_version": "1.0.0",
            "discovery_id": self.discovery_id,
            "created_at": self.created_at,
            "discovery_version": self.discovery_version,
            "signal": self.signal.to_dict(),
            "brand_evaluation": self.brand_evaluation.to_dict(),
            "opportunity": self.opportunity.to_dict(),
            "idea": (
                self.idea.to_dict()
                if self.idea is not None
                else None
            ),
            "processing": self.processing.to_dict(),
        }