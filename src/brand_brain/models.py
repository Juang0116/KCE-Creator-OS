from dataclasses import dataclass, field
from typing import Optional


@dataclass
class BrandEvaluation:
    brand_id: str
    signal_id: str

    relevant: bool
    relevance_score: float

    matched_pillars: list[str] = field(default_factory=list)
    matched_topics: list[str] = field(default_factory=list)

    reason: str = ""
    rule_flags: list[str] = field(default_factory=list)

    confidence: float = 0.0

    relevance_level: str = "irrelevant"

    dimensions: dict[str, float] = field(
        default_factory=lambda: {
            "pillar_fit": 0.0,
            "topic_fit": 0.0,
            "audience_fit": 0.0,
            "brand_promise_fit": 0.0,
            "context_fit": 0.0,
        }
    )

    positive_reasons: list[str] = field(default_factory=list)
    negative_reasons: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "brand_id": self.brand_id,
            "signal_id": self.signal_id,
            "relevant": self.relevant,
            "relevance_score": self.relevance_score,
            "relevance_level": self.relevance_level,
            "matched_pillars": self.matched_pillars,
            "matched_topics": self.matched_topics,
            "reason": self.reason,
            "rule_flags": self.rule_flags,
            "confidence": self.confidence,
            "dimensions": self.dimensions,
            "positive_reasons": self.positive_reasons,
            "negative_reasons": self.negative_reasons,
        }