from datetime import datetime, timezone

from .models import (
    LearningInsight,
    LearningProcessing,
    LearningRecord,
    LearningSource,
    LearningTarget,
)


class LearningEngineV0:
    """
    Deterministic V0 learning engine.

    Converts analytics metrics into simple,
    explainable insights. No ML or external APIs yet.
    """

    def generate(self, analytics_record) -> LearningRecord:
        now = datetime.now(timezone.utc).isoformat()

        metrics = analytics_record.metrics
        insights = []

        # Performance: CTR
        if metrics.impressions > 0:
            if metrics.ctr >= 0.10:
                insights.append(
                    LearningInsight(
                        insight_id="insight_ctr_strong",
                        category="performance",
                        observation="The content achieved a strong click-through rate.",
                        evidence=f"CTR: {metrics.ctr:.2%} from {metrics.impressions} impressions.",
                        confidence=0.9,
                        action="Prioritize similar packaging patterns in future content.",
                    )
                )
            elif metrics.ctr < 0.03:
                insights.append(
                    LearningInsight(
                        insight_id="insight_ctr_weak",
                        category="performance",
                        observation="The content achieved a low click-through rate.",
                        evidence=f"CTR: {metrics.ctr:.2%} from {metrics.impressions} impressions.",
                        confidence=0.9,
                        action="Review title and thumbnail patterns before repeating this format.",
                    )
                )

        # Audience: engagement
        if metrics.views > 0:
            engagement_actions = metrics.likes + metrics.comments + metrics.shares
            engagement_rate = engagement_actions / metrics.views

            if engagement_rate >= 0.05:
                insights.append(
                    LearningInsight(
                        insight_id="insight_engagement_strong",
                        category="audience",
                        observation="The content generated strong audience engagement.",
                        evidence=(
                            f"{engagement_actions} interactions from "
                            f"{metrics.views} views "
                            f"({engagement_rate:.2%})."
                        ),
                        confidence=0.85,
                        action="Explore additional content around this audience response.",
                    )
                )

        # Monetization
        if metrics.revenue > 0:
            insights.append(
                LearningInsight(
                    insight_id="insight_revenue_present",
                    category="monetization",
                    observation="The content generated measurable revenue.",
                    evidence=f"Revenue: {metrics.revenue:.2f}.",
                    confidence=1.0,
                    action="Track this content pattern for future monetization opportunities.",
                )
            )

        # Fallback when no deterministic threshold is triggered
        if not insights:
            insights.append(
                LearningInsight(
                    insight_id="insight_insufficient_signal",
                    category="performance",
                    observation="No strong deterministic learning signal was detected.",
                    evidence=(
                        f"Views: {metrics.views}, "
                        f"Impressions: {metrics.impressions}, "
                        f"CTR: {metrics.ctr:.2%}."
                    ),
                    confidence=0.5,
                    action="Collect more data before making strategic changes.",
                )
            )

        source = LearningSource(
            analytics_id=analytics_record.analytics_id,
            publish_plan_id=analytics_record.source.publish_plan_id,
            approval_id=analytics_record.source.approval_id,
            production_plan_id=analytics_record.source.production_plan_id,
            thumbnail_plan_id=analytics_record.source.thumbnail_plan_id,
            metadata_plan_id=analytics_record.source.metadata_plan_id,
            storyboard_id=analytics_record.source.storyboard_id,
            script_id=analytics_record.source.script_id,
            idea_id=analytics_record.source.idea_id,
            opportunity_id=analytics_record.source.opportunity_id,
            signal_id=analytics_record.source.signal_id,
        )

        target = LearningTarget(
            brand_id=analytics_record.target.brand_id,
            channel=analytics_record.target.channel,
            platform=analytics_record.target.platform,
            content_id=analytics_record.target.content_id,
        )

        processing = LearningProcessing(
            status="generated",
            confidence=1.0,
            processed_at=now,
        )

        return LearningRecord(
            schema_version=1.0,
            learning_id=f"learning_{analytics_record.target.content_id}",
            created_at=now,
            learning_version="1",
            source=source,
            target=target,
            insights=insights,
            processing=processing,
        )