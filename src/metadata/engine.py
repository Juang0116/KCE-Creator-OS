from datetime import datetime, timezone

from .models import (
    Metadata,
    MetadataPlan,
    MetadataProcessing,
    MetadataSource,
    MetadataTarget,
)


class MetadataEngineV0:
    """
    Deterministic V0 metadata planning engine.

    Converts thumbnail/production context into structured
    publication metadata. It does not publish content.
    """

    def generate(self, thumbnail_plan):
        source = MetadataSource(
            thumbnail_plan_id=thumbnail_plan.thumbnail_plan_id,
            production_plan_id=thumbnail_plan.source.production_plan_id,
            storyboard_id=thumbnail_plan.source.storyboard_id,
            script_id=thumbnail_plan.source.script_id,
            idea_id=thumbnail_plan.source.idea_id,
            opportunity_id=thumbnail_plan.source.opportunity_id,
            signal_id=thumbnail_plan.source.signal_id,
        )

        target = MetadataTarget(
            brand_id=thumbnail_plan.target.brand_id,
            channel=thumbnail_plan.target.channel,
            platform=thumbnail_plan.target.platform,
        )

        title = thumbnail_plan.thumbnail.text or "Untitled Content"

        metadata = Metadata(
            title=title,
            description=(
                f"Explore {title}. "
                "This video provides useful context, insights, "
                "and practical information about the topic."
            ),
            keywords=[
                title,
                thumbnail_plan.target.channel,
                thumbnail_plan.target.platform,
            ],
            category="Education",
            cta="Subscribe for more content.",
            language="en",
            status="planned",
        )

        processed_at = datetime.now(timezone.utc).isoformat()

        processing = MetadataProcessing(
            status="draft",
            confidence=0.8,
            processed_at=processed_at,
        )

        return MetadataPlan(
            schema_version="1.0",
            metadata_plan_id="metadata_plan_001",
            created_at=processed_at,
            metadata_plan_version="1",
            source=source,
            target=target,
            metadata=metadata,
            processing=processing,
        )