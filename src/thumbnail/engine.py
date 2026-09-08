from datetime import datetime, timezone

from .models import (
    Thumbnail,
    ThumbnailPlan,
    ThumbnailProcessing,
    ThumbnailSource,
    ThumbnailTarget,
)


class ThumbnailEngineV0:
    """
    Deterministic V0 thumbnail planning engine.

    Converts production context into a structured thumbnail plan.
    It does not generate the actual thumbnail image.
    """

    def generate(self, production_plan):
        source = ThumbnailSource(
            production_plan_id=production_plan.production_plan_id,
            storyboard_id=production_plan.source.storyboard_id,
            script_id=production_plan.source.script_id,
            idea_id=production_plan.source.idea_id,
            opportunity_id=production_plan.source.opportunity_id,
            signal_id=production_plan.source.signal_id,
        )

        target = ThumbnailTarget(
            brand_id=production_plan.source.brand_id,
            channel=production_plan.source.channel,
            platform=production_plan.source.platform,
        )

        title = getattr(production_plan, "title", "Untitled Content")

        thumbnail = Thumbnail(
            thumbnail_id="thumbnail_001",
            concept=f"High-impact visual representation of: {title}",
            visual_direction=(
                "Create a clear focal point, strong visual hierarchy, "
                "high contrast, and immediate topic recognition."
            ),
            text=title,
            composition=(
                "Single dominant subject, supporting visual elements, "
                "and concise readable text."
            ),
            assets=[],
            status="planned",
        )

        processing = ThumbnailProcessing(
            status="draft",
            confidence=0.8,
            processed_at=datetime.now(timezone.utc).isoformat(),
        )

        return ThumbnailPlan(
            schema_version="1.0",
            thumbnail_plan_id="thumbnail_plan_001",
            created_at=datetime.now(timezone.utc).isoformat(),
            thumbnail_plan_version="1",
            source=source,
            target=target,
            thumbnail=thumbnail,
            processing=processing,
        )