from dataclasses import dataclass, field
from typing import List


@dataclass
class MetadataSource:
    thumbnail_plan_id: str
    production_plan_id: str
    storyboard_id: str
    script_id: str
    idea_id: str
    opportunity_id: str
    signal_id: str

    def to_dict(self):
        return {
            "thumbnail_plan_id": self.thumbnail_plan_id,
            "production_plan_id": self.production_plan_id,
            "storyboard_id": self.storyboard_id,
            "script_id": self.script_id,
            "idea_id": self.idea_id,
            "opportunity_id": self.opportunity_id,
            "signal_id": self.signal_id,
        }


@dataclass
class MetadataTarget:
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
class Metadata:
    title: str
    description: str
    keywords: List[str] = field(default_factory=list)
    category: str = ""
    cta: str = ""
    language: str = ""
    status: str = "planned"

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "keywords": self.keywords,
            "category": self.category,
            "cta": self.cta,
            "language": self.language,
            "status": self.status,
        }


@dataclass
class MetadataProcessing:
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
class MetadataPlan:
    schema_version: str
    metadata_plan_id: str
    created_at: str
    metadata_plan_version: str
    source: MetadataSource
    target: MetadataTarget
    metadata: Metadata
    processing: MetadataProcessing

    def to_dict(self):
        return {
            "schema_version": self.schema_version,
            "metadata_plan_id": self.metadata_plan_id,
            "created_at": self.created_at,
            "metadata_plan_version": self.metadata_plan_version,
            "source": self.source.to_dict(),
            "target": self.target.to_dict(),
            "metadata": self.metadata.to_dict(),
            "processing": self.processing.to_dict(),
        }
    