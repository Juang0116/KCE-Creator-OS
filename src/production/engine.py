from datetime import datetime, timezone

from .models import (
    ProductionPlan,
    ProductionPlanSource,
    ProductionPlanTarget,
    ProductionProcessing,
    ProductionTimelineItem,
)


class ProductionEngineV0:
    """
    Deterministic Production Engine V0.

    Combines Storyboard, Asset Plan, Voice Plan and Music/SFX Plan
    into a structured production timeline.

    V0 does not render video. It creates the production instructions
    required by a future rendering layer.
    """

    def generate(
        self,
        storyboard,
        asset_plan,
        voice_plan,
        music_sfx_plan,
    ) -> ProductionPlan:

        created_at = datetime.now(timezone.utc).isoformat()

        source = ProductionPlanSource(
            storyboard_id=storyboard.storyboard_id,
            asset_plan_id=asset_plan.asset_plan_id,
            voice_plan_id=voice_plan.voice_plan_id,
            music_sfx_plan_id=music_sfx_plan.music_sfx_plan_id,
            script_id=storyboard.source.script_id,
            idea_id=storyboard.source.idea_id,
            opportunity_id=storyboard.source.opportunity_id,
            signal_id=storyboard.source.signal_id,
        )

        target = ProductionPlanTarget(
            brand_id=storyboard.target.brand_id,
            channel=storyboard.target.channel,
            platform=storyboard.target.platform,
        )

        timeline = []

        current_time = 0.0

        for scene in storyboard.scenes:
            duration = float(scene.estimated_duration_seconds)

            scene_asset_ids = [
                asset.asset_id
                for asset in asset_plan.assets
                if asset.scene_id == scene.scene_id
            ]

            scene_voice_ids = [
                segment.segment_id
                for segment in voice_plan.segments
                if segment.section_id == scene.section_id
            ]

            scene_audio_ids = [
                track.track_id
                for track in music_sfx_plan.tracks
                if track.scene_id == scene.scene_id
            ]

            timeline.append(
                ProductionTimelineItem(
                    timeline_id=f"timeline_{scene.scene_id}",
                    scene_id=scene.scene_id,
                    start_time_seconds=current_time,
                    end_time_seconds=current_time + duration,
                    asset_ids=scene_asset_ids,
                    voice_segment_ids=scene_voice_ids,
                    music_sfx_track_ids=scene_audio_ids,
                    transition=scene.transition,
                    status="planned",
                )
            )

            current_time += duration

        return ProductionPlan(
            schema_version="1.0",
            production_plan_id=f"production_plan_{storyboard.storyboard_id}",
            created_at=created_at,
            production_plan_version="1",
            source=source,
            target=target,
            timeline=timeline,
            processing=ProductionProcessing(
                status="draft",
                confidence=1.0,
                processed_at=created_at,
            ),
        )