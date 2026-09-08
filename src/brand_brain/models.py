from dataclasses import dataclass, field


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

    def to_dict(self) -> dict:
        return {
            "brand_id": self.brand_id,
            "signal_id": self.signal_id,
            "relevant": self.relevant,
            "relevance_score": self.relevance_score,
            "matched_pillars": self.matched_pillars,
            "matched_topics": self.matched_topics,
            "reason": self.reason,
            "rule_flags": self.rule_flags,
            "confidence": self.confidence,
        }