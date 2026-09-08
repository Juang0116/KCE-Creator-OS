from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ResearchSource:
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
class ResearchFinding:
    claim: str
    evidence: str
    source_id: str
    confidence: float

    def to_dict(self) -> dict:
        return {
            "claim": self.claim,
            "evidence": self.evidence,
            "source_id": self.source_id,
            "confidence": self.confidence,
        }


@dataclass
class ResearchObjective:
    research_question: str
    content_goal: str
    key_questions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "research_question": self.research_question,
            "content_goal": self.content_goal,
            "key_questions": self.key_questions,
        }


@dataclass
class ResearchScope:
    topics: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    exclusions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "topics": self.topics,
            "keywords": self.keywords,
            "exclusions": self.exclusions,
        }


@dataclass
class ResearchProcessing:
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
class ResearchBrief:
    research_id: str
    created_at: str
    research_version: str
    idea_id: str
    opportunity_id: str
    signal_id: str
    brand_id: str
    channel: str
    platform: str
    objective: ResearchObjective
    scope: ResearchScope
    findings: list[ResearchFinding] = field(default_factory=list)
    sources: list[ResearchSource] = field(default_factory=list)
    research_gaps: list[str] = field(default_factory=list)
    processing: ResearchProcessing = field(
        default_factory=ResearchProcessing
    )

    def to_dict(self) -> dict:
        return {
            "schema_version": "1.0.0",
            "research_id": self.research_id,
            "created_at": self.created_at,
            "research_version": self.research_version,
            "source": {
                "idea_id": self.idea_id,
                "opportunity_id": self.opportunity_id,
                "signal_id": self.signal_id,
            },
            "target": {
                "brand_id": self.brand_id,
                "channel": self.channel,
                "platform": self.platform,
            },
            "objective": self.objective.to_dict(),
            "scope": self.scope.to_dict(),
            "findings": [
                finding.to_dict()
                for finding in self.findings
            ],
            "sources": [
                source.to_dict()
                for source in self.sources
            ],
            "research_gaps": self.research_gaps,
            "processing": self.processing.to_dict(),
        }