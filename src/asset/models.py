from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AssetPlanSource:
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
class AssetPlanTarget:
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
class AssetRequirement:
    asset_id: str
    scene_id: str
    asset_type: str
    description: str
    purpose: str
    source_strategy: str
    priority: str
    status: str
    required: bool

    def to_dict(self) -> dict:
        return {
            "asset_id": self.asset_id,
            "scene_id": self.scene_id,
            "asset_type": self.asset_type,
            "description": self.description,
            "purpose": self.purpose,
            "source_strategy": self.source_strategy,
            "priority": self.priority,
            "status": self.status,
            "required": self.required,
        }


@dataclass
class AssetPlanProcessing:
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
class AssetPlan:
    schema_version: str
    asset_plan_id: str
    created_at: str
    asset_plan_version: str
    source: AssetPlanSource
    target: AssetPlanTarget
    assets: list[AssetRequirement] = field(default_factory=list)
    processing: AssetPlanProcessing = field(
        default_factory=lambda: AssetPlanProcessing(
            status="draft",
            confidence=0.0,
            processed_at=None,
        )
    )

    def to_dict(self) -> dict:
        return {
            "schema_version": self.schema_version,
            "asset_plan_id": self.asset_plan_id,
            "created_at": self.created_at,
            "asset_plan_version": self.asset_plan_version,
            "source": self.source.to_dict(),
            "target": self.target.to_dict(),
            "assets": [asset.to_dict() for asset in self.assets],
            "processing": self.processing.to_dict(),
        }