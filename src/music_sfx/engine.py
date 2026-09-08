from datetime import datetime, timezone

from .models import (
    MusicSFXPlan,
    MusicSFXPlanSource,
    MusicSFXPlanTarget,
    MusicSFXProcessing,
    MusicSFXTrack,
)


class MusicSFXEngineV0:
    """
    Deterministic Music/SFX Engine V0.

    Converts a Storyboard into a structured Music/SFX Plan.
    V0 does not generate or retrieve audio. It plans the
    audio requirements needed by a future production layer.
    """

    def generate(self, storyboard) -> MusicSFXPlan:
        created_at = datetime.now(timezone.utc).isoformat()

        source = MusicSFXPlanSource(
            storyboard_id=storyboard.storyboard_id,
            script_id=storyboard.source.script_id,
            idea_id=storyboard.source.idea_id,
            opportunity_id=storyboard.source.opportunity_id,
            signal_id=storyboard.source.signal_id,
        )

        target = MusicSFXPlanTarget(
            brand_id=storyboard.target.brand_id,
            channel=storyboard.target.channel,
            platform=storyboard.target.platform,
        )

        tracks = []

        for scene in storyboard.scenes:
            scene_duration = scene.estimated_duration_seconds

            tracks.append(
                MusicSFXTrack(
                    track_id=f"music_{scene.scene_id}",
                    scene_id=scene.scene_id,
                    track_type="music",
                    description="Background music appropriate for the scene.",
                    purpose="Support the emotional tone and pacing.",
                    source_strategy="retrieve",
                    priority="medium",
                    status="needed",
                    start_time_seconds=0.0,
                    end_time_seconds=float(scene_duration),
                )
            )

            if scene.transition.strip():
                tracks.append(
                    MusicSFXTrack(
                        track_id=f"sfx_{scene.scene_id}",
                        scene_id=scene.scene_id,
                        track_type="transition",
                        description="Transition sound effect for the scene change.",
                        purpose="Reinforce visual and narrative transitions.",
                        source_strategy="retrieve",
                        priority="low",
                        status="needed",
                        start_time_seconds=0.0,
                        end_time_seconds=min(2.0, float(scene_duration)),
                    )
                )

        return MusicSFXPlan(
            schema_version="1.0",
            music_sfx_plan_id=f"music_sfx_plan_{storyboard.storyboard_id}",
            created_at=created_at,
            music_sfx_plan_version="1",
            source=source,
            target=target,
            tracks=tracks,
            processing=MusicSFXProcessing(
                status="draft",
                confidence=1.0,
                processed_at=created_at,
            ),
        )