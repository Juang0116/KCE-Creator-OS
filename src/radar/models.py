from dataclasses import dataclass, field
from typing import Optional


@dataclass
class RadarSignal:
    signal_id: str
    detected_at: str
    radar_version: str

    source_type: str
    platform: str
    url: Optional[str]
    author: Optional[str]
    published_at: Optional[str]

    title: str
    summary: str
    keywords: list[str] = field(default_factory=list)
    topics: list[str] = field(default_factory=list)
    language: str = "es"

    evidence: dict = field(default_factory=dict)

    niches: list[str] = field(default_factory=list)
    relevance_reason: str = ""

    status: str = "detected"
    confidence: float = 0.0
    processed_at: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "schema_version": "1.0.0",
            "signal_id": self.signal_id,
            "detected_at": self.detected_at,
            "radar_version": self.radar_version,
            "source": {
                "type": self.source_type,
                "platform": self.platform,
                **({"url": self.url} if self.url is not None else {}),
                **({"author": self.author} if self.author is not None else {}),
                **(
                    {"published_at": self.published_at}
                    if self.published_at is not None
                    else {}
                ),
            },
            "signal": {
                "title": self.title,
                "summary": self.summary,
                "keywords": self.keywords,
                "topics": self.topics,
                "language": self.language,
            },
            "evidence": self.evidence,
            "relevance": {
                "niches": self.niches,
                "relevance_reason": self.relevance_reason,
            },
            "processing": {
                "status": self.status,
                "confidence": self.confidence,
                **(
                    {"processed_at": self.processed_at}
                    if self.processed_at is not None
                    else {}
                ),
            },
        }