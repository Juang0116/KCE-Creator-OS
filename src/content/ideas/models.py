from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ContentConcept:
    working_title: str
    hook: str
    core_promise: str
    angle: str
    format: str
    estimated_duration_seconds: int
    content_pillar: str

    def to_dict(self) -> dict:
        return {
            "working_title": self.working_title,
            "hook": self.hook,
            "core_promise": self.core_promise,
            "angle": self.angle,
            "format": self.format,
            "estimated_duration_seconds": self.estimated_duration_seconds,
            "content_pillar": self.content_pillar,
        }


@dataclass
class ContentAudience:
    target: str
    audience_need: str
    expected_value: str

    def to_dict(self) -> dict:
        return {
            "target": self.target,
            "audience_need": self.audience_need,
            "expected_value": self.expected_value,
        }


@dataclass
class CreativeDirection:
    storytelling_approach: str
    visual_direction: str
    voice_direction: str
    key_elements: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "storytelling_approach": self.storytelling_approach,
            "visual_direction": self.visual_direction,
            "voice_direction": self.voice_direction,
            "key_elements": self.key_elements,
        }


@dataclass
class ContentProduction:
    complexity: str
    estimated_production_hours: float
    required_assets: list[str] = field(default_factory=list)
    ai_assistance: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "complexity": self.complexity,
            "estimated_production_hours": self.estimated_production_hours,
            "required_assets": self.required_assets,
            "ai_assistance": self.ai_assistance,
        }


@dataclass
class ContentProcessing:
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
class ContentIdea:
    idea_id: str
    created_at: str
    idea_version: str

    opportunity_id: str
    signal_id: str

    brand_id: str
    channel: str
    platform: str

    concept: ContentConcept
    audience: ContentAudience
    creative_direction: CreativeDirection
    production: ContentProduction
    processing: ContentProcessing

    def to_dict(self) -> dict:
        return {
            "schema_version": "1.0.0",
            "idea_id": self.idea_id,
            "created_at": self.created_at,
            "idea_version": self.idea_version,
            "source": {
                "opportunity_id": self.opportunity_id,
                "signal_id": self.signal_id,
            },
            "target": {
                "brand_id": self.brand_id,
                "channel": self.channel,
                "platform": self.platform,
            },
            "concept": self.concept.to_dict(),
            "audience": self.audience.to_dict(),
            "creative_direction": self.creative_direction.to_dict(),
            "production": self.production.to_dict(),
            "processing": self.processing.to_dict(),
        }