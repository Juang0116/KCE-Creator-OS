from dataclasses import dataclass, field
from typing import List


@dataclass
class LearningSource:
    analytics_id: str
    publish_plan_id: str
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
            "analytics_id": self.analytics_id,
            "publish_plan_id": self.publish_plan_id,
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
class LearningTarget:
    brand_id: str
    channel: str
    platform: str
    content_id: str

    def to_dict(self):
        return {
            "brand_id": self.brand_id,
            "channel": self.channel,
            "platform": self.platform,
            "content_id": self.content_id,
        }


@dataclass
class LearningInsight:
    insight_id: str
    category: str
    observation: str
    evidence: str
    confidence: float
    action: str

    def to_dict(self):
        return {
            "insight_id": self.insight_id,
            "category": self.category,
            "observation": self.observation,
            "evidence": self.evidence,
            "confidence": self.confidence,
            "action": self.action,
        }


@dataclass
class LearningProcessing:
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
class LearningRecord:
    schema_version: float
    learning_id: str
    created_at: str
    learning_version: str
    source: LearningSource
    target: LearningTarget
    insights: List[LearningInsight] = field(default_factory=list)
    processing: LearningProcessing = field(
        default_factory=LearningProcessing
    )

    def to_dict(self):
        return {
            "schema_version": self.schema_version,
            "learning_id": self.learning_id,
            "created_at": self.created_at,
            "learning_version": self.learning_version,
            "source": self.source.to_dict(),
            "target": self.target.to_dict(),
            "insights": [insight.to_dict() for insight in self.insights],
            "processing": self.processing.to_dict(),
        }