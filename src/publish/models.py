from dataclasses import dataclass, field
from typing import List


@dataclass
class PublishSource:
    approval_id: str
    production_plan_id: str
    thumbnail_plan_id: str
    metadata_plan_id: str
    storyboard_id: str
    script_id: str
    idea_id: str
    opportunity_id: str
    signal_id: str

    def to_dict(self):
        return {
            "approval_id": self.approval_id,
            "production_plan_id": self.production_plan_id,
            "thumbnail_plan_id": self.thumbnail_plan_id,
            "metadata_plan_id": self.metadata_plan_id,
            "storyboard_id": self.storyboard_id,
            "script_id": self.script_id,
            "idea_id": self.idea_id,
            "opportunity_id": self.opportunity_id,
            "signal_id": self.signal_id,
        }


@dataclass
class PublishTarget:
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
class Publication:
    title: str
    description: str
    keywords: List[str] = field(default_factory=list)
    category: str = ""
    cta: str = ""
    language: str = ""
    visibility: str = "private"
    scheduled_at: str = ""
    status: str = "blocked"

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "keywords": self.keywords,
            "category": self.category,
            "cta": self.cta,
            "language": self.language,
            "visibility": self.visibility,
            "scheduled_at": self.scheduled_at,
            "status": self.status,
        }


@dataclass
class PublishProcessing:
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
class PublishPlan:
    schema_version: str
    publish_plan_id: str
    created_at: str
    publish_plan_version: str
    source: PublishSource
    target: PublishTarget
    publication: Publication
    processing: PublishProcessing

    def to_dict(self):
        return {
            "schema_version": self.schema_version,
            "publish_plan_id": self.publish_plan_id,
            "created_at": self.created_at,
            "publish_plan_version": self.publish_plan_version,
            "source": self.source.to_dict(),
            "target": self.target.to_dict(),
            "publication": self.publication.to_dict(),
            "processing": self.processing.to_dict(),
        }