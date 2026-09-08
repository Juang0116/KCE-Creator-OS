from dataclasses import dataclass, field
from typing import Optional


@dataclass
class MusicSFXPlanSource:
    storyboard_id: str
    script_id: str
    idea_id: str
    opportunity_id: str
    signal_id: str

    def to_dict(self) -> dict:
        return {
            "storyboard_id": self.storyboard_id,
            "script_id": self.script_id,
            "idea_id": self.idea_id,
            "opportunity_id": self.opportunity_id,
            "signal_id": self.signal_id,
        }


@dataclass
class MusicSFXPlanTarget:
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
class MusicSFXTrack:
    track_id: str
    scene_id: str
    track_type: str
    description: str
    purpose: str
    source_strategy: str
    priority: str
    status: str
    start_time_seconds: float
    end_time_seconds: float

    def to_dict(self) -> dict:
        return {
            "track_id": self.track_id,
            "scene_id": self.scene_id,
            "track_type": self.track_type,
            "description": self.description,
            "purpose": self.purpose,
            "source_strategy": self.source_strategy,
            "priority": self.priority,
            "status": self.status,
            "start_time_seconds": self.start_time_seconds,
            "end_time_seconds": self.end_time_seconds,
        }


@dataclass
class MusicSFXProcessing:
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
class MusicSFXPlan:
    schema_version: str
    music_sfx_plan_id: str
    created_at: str
    music_sfx_plan_version: str
    source: MusicSFXPlanSource
    target: MusicSFXPlanTarget
    tracks: list[MusicSFXTrack] = field(default_factory=list)
    processing: MusicSFXProcessing = field(
        default_factory=lambda: MusicSFXProcessing(
            status="draft",
            confidence=0.0,
            processed_at=None,
        )
    )

    def to_dict(self) -> dict:
        return {
            "schema_version": self.schema_version,
            "music_sfx_plan_id": self.music_sfx_plan_id,
            "created_at": self.created_at,
            "music_sfx_plan_version": self.music_sfx_plan_version,
            "source": self.source.to_dict(),
            "target": self.target.to_dict(),
            "tracks": [track.to_dict() for track in self.tracks],
            "processing": self.processing.to_dict(),
        }