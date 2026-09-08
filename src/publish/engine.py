from datetime import datetime, timezone

from .models import (
    Publication,
    PublishPlan,
    PublishProcessing,
    PublishSource,
    PublishTarget,
)


class PublishEngineV0:
    """
    Deterministic V0 publication preparation engine.

    Prepares a publication package only when human approval
    has been granted. It does not call external APIs or publish
    content.
    """

    def generate(
        self,
        approval_plan,
        production_plan,
        thumbnail_plan,
        metadata_plan,
    ):
        processed_at = datetime.now(timezone.utc).isoformat()

        source = PublishSource(
            approval_id=approval_plan.approval_id,
            production_plan_id=production_plan.production_plan_id,
            thumbnail_plan_id=thumbnail_plan.thumbnail_plan_id,
            metadata_plan_id=metadata_plan.metadata_plan_id,
            storyboard_id=thumbnail_plan.source.storyboard_id,
            script_id=thumbnail_plan.source.script_id,
            idea_id=thumbnail_plan.source.idea_id,
            opportunity_id=thumbnail_plan.source.opportunity_id,
            signal_id=thumbnail_plan.source.signal_id,
        )

        target = PublishTarget(
            brand_id=thumbnail_plan.target.brand_id,
            channel=thumbnail_plan.target.channel,
            platform=thumbnail_plan.target.platform,
        )

        approved = approval_plan.decision.status == "approved"

        if approved:
            publication_status = "ready"
            processing_status = "approved"
            confidence = 1.0
        else:
            publication_status = "blocked"
            processing_status = "review"
            confidence = 0.0

        metadata = metadata_plan.metadata

        publication = Publication(
            title=metadata.title,
            description=metadata.description,
            keywords=list(metadata.keywords),
            category=metadata.category,
            cta=metadata.cta,
            language=metadata.language,
            visibility="private",
            scheduled_at="",
            status=publication_status,
        )

        processing = PublishProcessing(
            status=processing_status,
            confidence=confidence,
            processed_at=processed_at,
        )

        return PublishPlan(
            schema_version="1.0",
            publish_plan_id="publish_plan_001",
            created_at=processed_at,
            publish_plan_version="1",
            source=source,
            target=target,
            publication=publication,
            processing=processing,
        )