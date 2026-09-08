from datetime import datetime, timezone

from .models import (
    VoicePlan,
    VoicePlanProcessing,
    VoicePlanSource,
    VoicePlanTarget,
    VoiceProfile,
    VoiceSegment,
)


class VoiceEngineV0:
    """
    Deterministic Voice Engine V0.

    Converts a Script into a structured Voice Plan.
    V0 does not generate audio. It prepares the narration
    segments and metadata required by a future TTS layer.
    """

    def generate(
        self,
        script,
        voice_profile: VoiceProfile,
    ) -> VoicePlan:

        created_at = datetime.now(timezone.utc).isoformat()

        source = VoicePlanSource(
            script_id=script.script_id,
            storyboard_id="",
            idea_id=script.source.idea_id,
            opportunity_id=script.source.opportunity_id,
            signal_id=script.source.signal_id,
        )

        target = VoicePlanTarget(
            brand_id=script.target.brand_id,
            channel=script.target.channel,
            platform=script.target.platform,
        )

        segments = []

        segment_index = 1

        # Hook
        if script.hook.narration.strip():
            segments.append(
                VoiceSegment(
                    segment_id=f"voice_segment_{segment_index}",
                    section_id="hook",
                    text=script.hook.narration,
                    language=voice_profile.language,
                    emotion="engaging",
                    delivery="natural",
                    estimated_duration_seconds=self._estimate_duration(
                        script.hook.narration
                    ),
                    status="planned",
                )
            )
            segment_index += 1

        # Introduction
        if script.introduction.narration.strip():
            segments.append(
                VoiceSegment(
                    segment_id=f"voice_segment_{segment_index}",
                    section_id="introduction",
                    text=script.introduction.narration,
                    language=voice_profile.language,
                    emotion="clear",
                    delivery="natural",
                    estimated_duration_seconds=self._estimate_duration(
                        script.introduction.narration
                    ),
                    status="planned",
                )
            )
            segment_index += 1

        # Sections
        for section in script.sections:
            if not section.narration.strip():
                continue

            segments.append(
                VoiceSegment(
                    segment_id=f"voice_segment_{segment_index}",
                    section_id=section.section_id,
                    text=section.narration,
                    language=voice_profile.language,
                    emotion="informative",
                    delivery="natural",
                    estimated_duration_seconds=self._estimate_duration(
                        section.narration
                    ),
                    status="planned",
                )
            )
            segment_index += 1

        # Conclusion
        if script.conclusion.narration.strip():
            segments.append(
                VoiceSegment(
                    segment_id=f"voice_segment_{segment_index}",
                    section_id="conclusion",
                    text=script.conclusion.narration,
                    language=voice_profile.language,
                    emotion="conclusive",
                    delivery="natural",
                    estimated_duration_seconds=self._estimate_duration(
                        script.conclusion.narration
                    ),
                    status="planned",
                )
            )
            segment_index += 1

        # CTA
        if script.cta.narration.strip():
            segments.append(
                VoiceSegment(
                    segment_id=f"voice_segment_{segment_index}",
                    section_id="cta",
                    text=script.cta.narration,
                    language=voice_profile.language,
                    emotion="inviting",
                    delivery="natural",
                    estimated_duration_seconds=self._estimate_duration(
                        script.cta.narration
                    ),
                    status="planned",
                )
            )

        return VoicePlan(
            schema_version="1.0",
            voice_plan_id=f"voice_plan_{script.script_id}",
            created_at=created_at,
            voice_plan_version="1",
            source=source,
            target=target,
            voice_profile=voice_profile,
            segments=segments,
            processing=VoicePlanProcessing(
                status="draft",
                confidence=1.0,
                processed_at=created_at,
            ),
        )

    @staticmethod
    def _estimate_duration(text: str) -> int:
        """
        Rough narration duration estimate.

        Assumes approximately 150 words per minute.
        Minimum duration is one second.
        """

        words = len(text.split())
        duration = round((words / 150) * 60)

        return max(1, duration)