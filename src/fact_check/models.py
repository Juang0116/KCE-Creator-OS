from dataclasses import dataclass, field
from typing import Optional


@dataclass
class FactCheckSource:
    source_id: str
    title: str
    url: str
    publisher: str
    source_type: str
    reliability: float

    def to_dict(self) -> dict:
        return {
            "source_id": self.source_id,
            "title": self.title,
            "url": self.url,
            "publisher": self.publisher,
            "source_type": self.source_type,
            "reliability": self.reliability,
        }


@dataclass
class FactCheckCheck:
    check_id: str
    claim: str
    evidence: str
    source_ids: list[str] = field(default_factory=list)
    verification_status: str = "unverified"
    confidence: float = 0.0
    notes: str = ""

    def to_dict(self) -> dict:
        return {
            "check_id": self.check_id,
            "claim": self.claim,
            "evidence": self.evidence,
            "source_ids": self.source_ids,
            "verification_status": self.verification_status,
            "confidence": self.confidence,
            "notes": self.notes,
        }


@dataclass
class FactCheckSummary:
    total_claims: int
    verified_claims: int
    partially_verified_claims: int
    unverified_claims: int
    refuted_claims: int
    conflicting_claims: int

    def to_dict(self) -> dict:
        return {
            "total_claims": self.total_claims,
            "verified_claims": self.verified_claims,
            "partially_verified_claims": self.partially_verified_claims,
            "unverified_claims": self.unverified_claims,
            "refuted_claims": self.refuted_claims,
            "conflicting_claims": self.conflicting_claims,
        }


@dataclass
class FactCheckProcessing:
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
class FactCheck:
    fact_check_id: str
    created_at: str
    fact_check_version: str

    research_id: str
    idea_id: str
    opportunity_id: str
    signal_id: str

    brand_id: str
    channel: str
    platform: str

    checks: list[FactCheckCheck] = field(default_factory=list)
    summary: FactCheckSummary = field(
        default_factory=lambda: FactCheckSummary(
            total_claims=0,
            verified_claims=0,
            partially_verified_claims=0,
            unverified_claims=0,
            refuted_claims=0,
            conflicting_claims=0,
        )
    )
    processing: FactCheckProcessing = field(
        default_factory=FactCheckProcessing
    )

    def to_dict(self) -> dict:
        return {
            "schema_version": "1.0.0",
            "fact_check_id": self.fact_check_id,
            "created_at": self.created_at,
            "fact_check_version": self.fact_check_version,
            "source": {
                "research_id": self.research_id,
                "idea_id": self.idea_id,
                "opportunity_id": self.opportunity_id,
                "signal_id": self.signal_id,
            },
            "target": {
                "brand_id": self.brand_id,
                "channel": self.channel,
                "platform": self.platform,
            },
            "checks": [
                check.to_dict()
                for check in self.checks
            ],
            "summary": self.summary.to_dict(),
            "processing": self.processing.to_dict(),
        }