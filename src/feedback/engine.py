from datetime import datetime, timezone

from .models import (
    FeedbackAction,
    FeedbackProcessing,
    FeedbackRecord,
    FeedbackSource,
    FeedbackTarget,
)


class FeedbackEngineV0:
    """
    Deterministic V0 feedback engine.

    Converts Learning insights into proposed actions.
    No automatic strategic changes are applied.
    """

    def generate(self, learning_record) -> FeedbackRecord:
        now = datetime.now(timezone.utc).isoformat()
        actions = []

        for index, insight in enumerate(learning_record.insights, start=1):
            if insight.category == "performance":
                if insight.insight_id == "insight_ctr_strong":
                    action_type = "reinforce"
                    priority = "high"
                elif insight.insight_id == "insight_ctr_weak":
                    action_type = "review"
                    priority = "high"
                else:
                    action_type = "collect_more_data"
                    priority = "medium"

            elif insight.category == "audience":
                action_type = "experiment"
                priority = "high"

            elif insight.category == "monetization":
                action_type = "reinforce"
                priority = "medium"

            else:
                action_type = "review"
                priority = "medium"

            actions.append(
                FeedbackAction(
                    action_id=f"action_{index}",
                    type=action_type,
                    reason=insight.action,
                    priority=priority,
                    status="proposed",
                )
            )

        if not actions:
            actions.append(
                FeedbackAction(
                    action_id="action_1",
                    type="collect_more_data",
                    reason="No learning actions were generated.",
                    priority="low",
                    status="proposed",
                )
            )

        source = FeedbackSource(
            learning_id=learning_record.learning_id,
            analytics_id=learning_record.source.analytics_id,
            opportunity_id=learning_record.source.opportunity_id,
            idea_id=learning_record.source.idea_id,
            signal_id=learning_record.source.signal_id,
        )

        target = FeedbackTarget(
            brand_id=learning_record.target.brand_id,
            channel=learning_record.target.channel,
            platform=learning_record.target.platform,
            content_id=learning_record.target.content_id,
        )

        processing = FeedbackProcessing(
            status="generated",
            confidence=1.0,
            processed_at=now,
        )

        return FeedbackRecord(
            schema_version="1.0",
            feedback_id=f"feedback_{learning_record.target.content_id}",
            created_at=now,
            feedback_version="1",
            source=source,
            target=target,
            actions=actions,
            processing=processing,
        )