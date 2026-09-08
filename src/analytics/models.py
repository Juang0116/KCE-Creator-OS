from dataclasses import dataclass


@dataclass
class AnalyticsSource:
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
class AnalyticsTarget:
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
class AnalyticsMetrics:
    views: int = 0
    impressions: int = 0
    ctr: float = 0.0
    watch_time_seconds: float = 0.0
    average_view_duration_seconds: float = 0.0
    likes: int = 0
    comments: int = 0
    shares: int = 0
    subscribers_gained: int = 0
    revenue: float = 0.0

    def to_dict(self):
        return {
            "views": self.views,
            "impressions": self.impressions,
            "ctr": self.ctr,
            "watch_time_seconds": self.watch_time_seconds,
            "average_view_duration_seconds": self.average_view_duration_seconds,
            "likes": self.likes,
            "comments": self.comments,
            "shares": self.shares,
            "subscribers_gained": self.subscribers_gained,
            "revenue": self.revenue,
        }


@dataclass
class AnalyticsProcessing:
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
class AnalyticsRecord:
    schema_version: str
    analytics_id: str
    created_at: str
    analytics_version: str
    source: AnalyticsSource
    target: AnalyticsTarget
    metrics: AnalyticsMetrics
    processing: AnalyticsProcessing

    def to_dict(self):
        return {
            "schema_version": self.schema_version,
            "analytics_id": self.analytics_id,
            "created_at": self.created_at,
            "analytics_version": self.analytics_version,
            "source": self.source.to_dict(),
            "target": self.target.to_dict(),
            "metrics": self.metrics.to_dict(),
            "processing": self.processing.to_dict(),
        }