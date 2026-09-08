from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ProductionPlanSource:
    storyboard_id: str
    asset_plan_id: str
    voice_plan_id: str
    music_sfx_plan_id: str
    script_id: str
    idea_id: str
    opportunity_id: str
    signal_id: str

    def to_dict(self) -> dict:
        return {
            "storyboard_id": self.storyboard_id,
            "asset_plan_id": self.asset_plan_id,
            "voice_plan_id": self.voice_plan_id,
            "music_sfx_plan_id": self.music_sfx_plan_id,
            "script_id": self.script_id,
            "idea_id": self.idea_id,
            "opportunity_id": self.opportunity_id,
            "signal_id": self.signal_id,
        }


@dataclass
class ProductionPlanTarget:
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
class ProductionTimelineItem:
    timeline_id: str
    scene_id: str
    start_time_seconds: float
    end_time_seconds: float
    asset_ids: list[str] = field(default_factory=list)
    voice_segment_ids: list[str] = field(default_factory=list)
    music_sfx_track_ids: list[str] = field(default_factory=list)
    transition: str = ""
    status: str = "planned"

    def to_dict(self) -> dict:
        return {
            "timeline_id": self.timeline_id,
            "scene_id": self.scene_id,
            "start_time_seconds": self.start_time_seconds,
            "end_time_seconds": self.end_time_seconds,
            "asset_ids": self.asset_ids,
            "voice_segment_ids": self.voice_segment_ids,
            "music_sfx_track_ids": self.music_sfx_track_ids,
            "transition": self.transition,
            "status": self.status,
        }


@dataclass
class ProductionProcessing:
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
class ProductionPlan:
    schema_version: str
    production_plan_id: str
    created_at: str
    production_plan_version: str
    source: ProductionPlanSource
    target: ProductionPlanTarget
    timeline: list[ProductionTimelineItem] = field(default_factory=list)
    processing: ProductionProcessing = field(
        default_factory=lambda: ProductionProcessing(
            status="draft",
            confidence=0.0,
            processed_at=None,
        )
    )

    def to_dict(self) -> dict:
        return {
            "schema_version": self.schema_version,
            "production_plan_id": self.production_plan_id,
            "created_at": self.created_at,
            "production_plan_version": self.production_plan_version,
            "source": self.source.to_dict(),
            "target": self.target.to_dict(),
            "timeline": [item.to_dict() for item in self.timeline],
            "processing": self.processing.to_dict(),
        }