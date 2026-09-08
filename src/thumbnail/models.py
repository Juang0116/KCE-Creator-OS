from dataclasses import dataclass, field
from typing import List


@dataclass
class ThumbnailSource:
    production_plan_id: str
    storyboard_id: str
    script_id: str
    idea_id: str
    opportunity_id: str
    signal_id: str

    def to_dict(self):
        return {
            "production_plan_id": self.production_plan_id,
            "storyboard_id": self.storyboard_id,
            "script_id": self.script_id,
            "idea_id": self.idea_id,
            "opportunity_id": self.opportunity_id,
            "signal_id": self.signal_id,
        }


@dataclass
class ThumbnailTarget:
    brand_id: str
    channel: str
    platform: str

    def to_dict(self):
        return {
            "brand_id": self.brand_id,
            "channel": self.channel,
            "platform": self.platform,
        }


@dataclass
class Thumbnail:
    thumbnail_id: str
    concept: str
    visual_direction: str
    text: str
    composition: str
    assets: List[str] = field(default_factory=list)
    status: str = "planned"

    def to_dict(self):
        return {
            "thumbnail_id": self.thumbnail_id,
            "concept": self.concept,
            "visual_direction": self.visual_direction,
            "text": self.text,
            "composition": self.composition,
            "assets": self.assets,
            "status": self.status,
        }


@dataclass
class ThumbnailProcessing:
    status: str = "draft"
    confidence: float = 0.0
    processed_at: str = ""

    def to_dict(self):
        return {
            "status": self.status,
            "confidence": self.confidence,
            "processed_at": self.processed_at,
        }


@dataclass
class ThumbnailPlan:
    schema_version: str
    thumbnail_plan_id: str
    created_at: str
    thumbnail_plan_version: str
    source: ThumbnailSource
    target: ThumbnailTarget
    thumbnail: Thumbnail
    processing: ThumbnailProcessing

    def to_dict(self):
        return {
            "schema_version": self.schema_version,
            "thumbnail_plan_id": self.thumbnail_plan_id,
            "created_at": self.created_at,
            "thumbnail_plan_version": self.thumbnail_plan_version,
            "source": self.source.to_dict(),
            "target": self.target.to_dict(),
            "thumbnail": self.thumbnail.to_dict(),
            "processing": self.processing.to_dict(),
        }