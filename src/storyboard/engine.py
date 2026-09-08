from datetime import datetime, timezone
from uuid import uuid4

from .models import (
    Storyboard,
    StoryboardMetadata,
    StoryboardProcessing,
    StoryboardScene,
    StoryboardSource,
    StoryboardTarget,
)


class StoryboardEngineV0:
    """
    Deterministic V0 storyboard generator.

    Converts a validated Script into a structured Storyboard.
    No AI, external APIs, or web access are used in V0.
    """

    def generate(self, script) -> Storyboard:
        storyboard_id = f"storyboard_{uuid4().hex[:12]}"
        created_at = datetime.now(timezone.utc).isoformat()

        source = StoryboardSource(
            script_id=script.script_id,
            idea_id=script.source.idea_id,
            research_id=script.source.research_id,
            fact_check_id=script.source.fact_check_id,
            opportunity_id=script.source.opportunity_id,
            signal_id=script.source.signal_id,
        )

        target = StoryboardTarget(
            brand_id=script.target.brand_id,
            channel=script.target.channel,
            platform=script.target.platform,
        )

        scenes = []

        # Hook
        scenes.append(
            StoryboardScene(
                scene_id="scene_hook",
                section_id="hook",
                narration=script.hook.narration,
                visual_direction=script.hook.visual_direction,
                shot_type="opening",
                visual_assets=["intro_graphics"],
                on_screen_text="",
                transition="cut",
                estimated_duration_seconds=10,
            )
        )

        # Introduction
        scenes.append(
            StoryboardScene(
                scene_id="scene_intro",
                section_id="introduction",
                narration=script.introduction.narration,
                visual_direction=script.introduction.visual_direction,
                shot_type="medium",
                visual_assets=["intro_graphics", "supporting_visuals"],
                on_screen_text="",
                transition="cut",
                estimated_duration_seconds=15,
            )
        )

        # Script sections
        for index, section in enumerate(script.sections, start=1):
            scenes.append(
                StoryboardScene(
                    scene_id=f"scene_{index}",
                    section_id=section.section_id,
                    narration=section.narration,
                    visual_direction=section.visual_direction,
                    shot_type="main",
                    visual_assets=["supporting_visuals"],
                    on_screen_text="",
                    transition=section.transition,
                    estimated_duration_seconds=max(
                        1,
                        round(
                            script.metadata.estimated_duration_seconds
                            / max(len(script.sections) + 2, 1)
                        ),
                    ),
                )
            )

        # Conclusion
        scenes.append(
            StoryboardScene(
                scene_id="scene_conclusion",
                section_id="conclusion",
                narration=script.conclusion.narration,
                visual_direction=script.conclusion.visual_direction,
                shot_type="closing",
                visual_assets=["supporting_visuals"],
                on_screen_text="",
                transition="fade",
                estimated_duration_seconds=15,
            )
        )

        # CTA
        scenes.append(
            StoryboardScene(
                scene_id="scene_cta",
                section_id="cta",
                narration=script.cta.narration,
                visual_direction=script.cta.visual_direction,
                shot_type="cta",
                visual_assets=["end_screen"],
                on_screen_text="",
                transition="fade_out",
                estimated_duration_seconds=10,
            )
        )

        metadata = StoryboardMetadata(
            title=script.metadata.title,
            format=script.metadata.format,
            estimated_duration_seconds=script.metadata.estimated_duration_seconds,
            scene_count=len(scenes),
        )

        processing = StoryboardProcessing(
            status="draft",
            confidence=script.processing.confidence,
            processed_at=None,
        )

        return Storyboard(
            schema_version="1.0",
            storyboard_id=storyboard_id,
            created_at=created_at,
            storyboard_version="1",
            source=source,
            target=target,
            metadata=metadata,
            scenes=scenes,
            processing=processing,
        )