from datetime import datetime, timezone
from typing import Optional

from .models import (
    AnalyticsMetrics,
    AnalyticsProcessing,
    AnalyticsRecord,
    AnalyticsSource,
    AnalyticsTarget,
)


class AnalyticsEngineV0:
    """
    Deterministic V0 analytics engine.

    Creates a structured analytics record from a PublishPlan.
    V0 does not connect to external platforms yet.
    """

    def generate(
        self,
        publish_plan,
        content_id: str,
        metrics: Optional[AnalyticsMetrics] = None,
    ) -> AnalyticsRecord:
        now = datetime.now(timezone.utc).isoformat()

        if metrics is None:
            metrics = AnalyticsMetrics(
                views=0,
                impressions=0,
                ctr=0.0,
                watch_time_seconds=0.0,
                average_view_duration_seconds=0.0,
                likes=0,
                comments=0,
                shares=0,
                subscribers_gained=0,
                revenue=0.0,
            )

        source = AnalyticsSource(
            publish_plan_id=publish_plan.publish_id,
            approval_id=publish_plan.source.approval_id,
            production_plan_id=publish_plan.source.production_plan_id,
            thumbnail_plan_id=publish_plan.source.thumbnail_plan_id,
            metadata_plan_id=publish_plan.source.metadata_plan_id,
            storyboard_id=publish_plan.source.storyboard_id,
            script_id=publish_plan.source.script_id,
            idea_id=publish_plan.source.idea_id,
            opportunity_id=publish_plan.source.opportunity_id,
            signal_id=publish_plan.source.signal_id,
        )

        target = AnalyticsTarget(
            brand_id=publish_plan.target.brand_id,
            channel=publish_plan.target.channel,
            platform=publish_plan.target.platform,
            content_id=content_id,
        )

        processing = AnalyticsProcessing(
            status="collected",
            confidence=1.0,
            processed_at=now,
        )

        return AnalyticsRecord(
            schema_version=1.0,
            analytics_id=f"analytics_{content_id}",
            created_at=now,
            analytics_version="1",
            source=source,
            target=target,
            metrics=metrics,
            processing=processing,
        )