from dataclasses import dataclass, field
from typing import Optional


@dataclass
class StoryboardSource:
    script_id: str
    idea_id: str
    research_id: str
    fact_check_id: str
    opportunity_id: str
    signal_id: str

    def to_dict(self) -> dict:
        return {
            "script_id": self.script_id,
            "idea_id": self.idea_id,
            "research_id": self.research_id,
            "fact_check_id": self.fact_check_id,
            "opportunity_id": self.opportunity_id,
            "signal_id": self.signal_id,
        }


@dataclass
class StoryboardTarget:
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
class StoryboardMetadata:
    title: str
    format: str
    estimated_duration_seconds: int
    scene_count: int

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "format": self.format,
            "estimated_duration_seconds": self.estimated_duration_seconds,
            "scene_count": self.scene_count,
        }


@dataclass
class StoryboardScene:
    scene_id: str
    section_id: str
    narration: str
    visual_direction: str
    shot_type: str
    visual_assets: list[str] = field(default_factory=list)
    on_screen_text: str = ""
    transition: str = ""
    estimated_duration_seconds: int = 1

    def to_dict(self) -> dict:
        return {
            "scene_id": self.scene_id,
            "section_id": self.section_id,
            "narration": self.narration,
            "visual_direction": self.visual_direction,
            "shot_type": self.shot_type,
            "visual_assets": self.visual_assets,
            "on_screen_text": self.on_screen_text,
            "transition": self.transition,
            "estimated_duration_seconds": self.estimated_duration_seconds,
        }


@dataclass
class StoryboardProcessing:
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
class Storyboard:
    schema_version: str
    storyboard_id: str
    created_at: str
    storyboard_version: str
    source: StoryboardSource
    target: StoryboardTarget
    metadata: StoryboardMetadata
    scenes: list[StoryboardScene] = field(default_factory=list)
    processing: StoryboardProcessing = field(
        default_factory=lambda: StoryboardProcessing(
            status="draft",
            confidence=0.0,
            processed_at=None,
        )
    )

    def to_dict(self) -> dict:
        return {
            "schema_version": self.schema_version,
            "storyboard_id": self.storyboard_id,
            "created_at": self.created_at,
            "storyboard_version": self.storyboard_version,
            "source": self.source.to_dict(),
            "target": self.target.to_dict(),
            "metadata": self.metadata.to_dict(),
            "scenes": [scene.to_dict() for scene in self.scenes],
            "processing": self.processing.to_dict(),
        }