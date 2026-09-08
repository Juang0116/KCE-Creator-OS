from dataclasses import dataclass, field
from typing import Optional


@dataclass
class OpportunityScoring:
    relevance: float
    audience_fit: float
    trend_strength: float
    novelty: float
    production_feasibility: float
    evergreen_potential: float
    total_score: float

    def to_dict(self) -> dict:
        return {
            "relevance": self.relevance,
            "audience_fit": self.audience_fit,
            "trend_strength": self.trend_strength,
            "novelty": self.novelty,
            "production_feasibility": self.production_feasibility,
            "evergreen_potential": self.evergreen_potential,
            "total_score": self.total_score,
        }


@dataclass
class OpportunityAnalysis:
    why_now: str
    why_this_brand: str
    risks: list[str] = field(default_factory=list)
    recommendation: str = "candidate"

    def to_dict(self) -> dict:
        return {
            "why_now": self.why_now,
            "why_this_brand": self.why_this_brand,
            "risks": self.risks,
            "recommendation": self.recommendation,
        }


@dataclass
class OpportunityProcessing:
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
class Opportunity:
    opportunity_id: str
    created_at: str
    opportunity_version: str
    signal_id: str
    brand_id: str
    channel: str
    scoring: OpportunityScoring
    analysis: OpportunityAnalysis
    processing: OpportunityProcessing

    def to_dict(self) -> dict:
        return {
            "schema_version": "1.0.0",
            "opportunity_id": self.opportunity_id,
            "created_at": self.created_at,
            "opportunity_version": self.opportunity_version,
            "source": {
                "signal_id": self.signal_id,
            },
            "target": {
                "brand_id": self.brand_id,
                "channel": self.channel,
            },
            "scoring": self.scoring.to_dict(),
            "analysis": self.analysis.to_dict(),
            "processing": self.processing.to_dict(),
        }