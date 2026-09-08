from dataclasses import dataclass, field
from typing import Optional


@dataclass
class VoicePlanSource:
    script_id: str
    storyboard_id: str
    idea_id: str
    opportunity_id: str
    signal_id: str

    def to_dict(self) -> dict:
        return {
            "script_id": self.script_id,
            "storyboard_id": self.storyboard_id,
            "idea_id": self.idea_id,
            "opportunity_id": self.opportunity_id,
            "signal_id": self.signal_id,
        }


@dataclass
class VoicePlanTarget:
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
class VoiceProfile:
    voice_id: str
    language: str
    tone: str
    style: str
    gender: str
    age_range: str

    def to_dict(self) -> dict:
        return {
            "voice_id": self.voice_id,
            "language": self.language,
            "tone": self.tone,
            "style": self.style,
            "gender": self.gender,
            "age_range": self.age_range,
        }


@dataclass
class VoiceSegment:
    segment_id: str
    section_id: str
    text: str
    language: str
    emotion: str
    delivery: str
    estimated_duration_seconds: int
    status: str

    def to_dict(self) -> dict:
        return {
            "segment_id": self.segment_id,
            "section_id": self.section_id,
            "text": self.text,
            "language": self.language,
            "emotion": self.emotion,
            "delivery": self.delivery,
            "estimated_duration_seconds": self.estimated_duration_seconds,
            "status": self.status,
        }


@dataclass
class VoicePlanProcessing:
    status: str
    confidence: float
    processed_at: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "confidence": self.confidence,
            "processed_at": self.processed_at,
        }


@dataclass
class VoicePlan:
    schema_version: str
    voice_plan_id: str
    created_at: str
    voice_plan_version: str
    source: VoicePlanSource
    target: VoicePlanTarget
    voice_profile: VoiceProfile
    segments: list[VoiceSegment] = field(default_factory=list)
    processing: VoicePlanProcessing = field(
        default_factory=lambda: VoicePlanProcessing(
            status="draft",
            confidence=0.0,
            processed_at=None,
        )
    )

    def to_dict(self) -> dict:
        return {
            "schema_version": self.schema_version,
            "voice_plan_id": self.voice_plan_id,
            "created_at": self.created_at,
            "voice_plan_version": self.voice_plan_version,
            "source": self.source.to_dict(),
            "target": self.target.to_dict(),
            "voice_profile": self.voice_profile.to_dict(),
            "segments": [
                segment.to_dict()
                for segment in self.segments
            ],
            "processing": self.processing.to_dict(),
        }