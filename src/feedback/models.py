from dataclasses import dataclass, field
from typing import List


@dataclass
class FeedbackSource:
    learning_id: str
    analytics_id: str
    opportunity_id: str
    idea_id: str
    signal_id: str

    def to_dict(self):
        return {
            "learning_id": self.learning_id,
            "analytics_id": self.analytics_id,
            "opportunity_id": self.opportunity_id,
            "idea_id": self.idea_id,
            "signal_id": self.signal_id,
        }


@dataclass
class FeedbackTarget:
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
class FeedbackAction:
    action_id: str
    type: str
    reason: str
    priority: str
    status: str

    def to_dict(self):
        return {
            "action_id": self.action_id,
            "type": self.type,
            "reason": self.reason,
            "priority": self.priority,
            "status": self.status,
        }


@dataclass
class FeedbackProcessing:
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
class FeedbackRecord:
    schema_version: float
    feedback_id: str
    created_at: str
    feedback_version: str
    source: FeedbackSource
    target: FeedbackTarget
    actions: List[FeedbackAction] = field(default_factory=list)
    processing: FeedbackProcessing = field(
        default_factory=FeedbackProcessing
    )

    def to_dict(self):
        return {
            "schema_version": self.schema_version,
            "feedback_id": self.feedback_id,
            "created_at": self.created_at,
            "feedback_version": self.feedback_version,
            "source": self.source.to_dict(),
            "target": self.target.to_dict(),
            "actions": [action.to_dict() for action in self.actions],
            "processing": self.processing.to_dict(),
        }