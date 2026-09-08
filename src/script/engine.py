from datetime import datetime, timezone
from uuid import uuid4

from src.content.ideas.models import ContentIdea
from src.research.models import ResearchBrief
from src.fact_check.models import FactCheck

from .models import (
    Script,
    ScriptSource,
    ScriptTarget,
    ScriptMetadata,
    ScriptHook,
    ScriptIntroduction,
    ScriptSection,
    ScriptClaim,
    ScriptConclusion,
    ScriptCTA,
    ScriptProcessing,
)


class ScriptEngineV0:
    """
    Deterministic V0 engine that converts:

    Content Idea + Research Brief + Fact Check
    -> Content Script
    """

    def generate(
        self,
        idea: ContentIdea,
        research: ResearchBrief,
        fact_check: FactCheck,
    ) -> Script:

        script_id = f"script_{uuid4().hex[:12]}"
        created_at = datetime.now(timezone.utc).isoformat()

        source = ScriptSource(
            idea_id=idea.idea_id,
            research_id=research.research_id,
            fact_check_id=fact_check.fact_check_id,
            opportunity_id=idea.opportunity_id,
            signal_id=idea.signal_id,
        )

        target = ScriptTarget(
            brand_id=idea.brand_id,
            channel=idea.channel,
            platform=idea.platform,
        )

        metadata = ScriptMetadata(
            title=idea.concept.working_title,
            format=idea.concept.format,
            estimated_duration_seconds=idea.concept.estimated_duration_seconds,
            content_pillar=idea.concept.content_pillar,
            tone=idea.creative_direction.voice_direction,
        )

        hook = ScriptHook(
            narration=idea.concept.hook,
            visual_direction=idea.creative_direction.visual_direction,
        )

        introduction = ScriptIntroduction(
            narration=(
                f"En este video vamos a explorar "
                f"{idea.concept.core_promise}"
            ),
            visual_direction=idea.creative_direction.visual_direction,
        )

        sections = []

        for index, check in enumerate(fact_check.checks, start=1):
            claims = [
                ScriptClaim(
                    claim=check.claim,
                    fact_check_id=fact_check.fact_check_id,
                    verification_status=check.verification_status,
                )
            ]

            sections.append(
                ScriptSection(
                    section_id=f"section_{index}",
                    title=f"Parte {index}",
                    narration=check.claim,
                    claims=claims,
                    visual_direction=(
                        idea.creative_direction.visual_direction
                    ),
                    transition="Continuemos con el siguiente punto.",
                )
            )

        conclusion = ScriptConclusion(
            narration=(
                "Ahora tenemos una visión más clara del tema "
                "y de los puntos principales que debemos recordar."
            ),
            visual_direction=idea.creative_direction.visual_direction,
        )

        cta = ScriptCTA(
            narration=(
                "Si te gustó este contenido, "
                "suscríbete para descubrir más."
            ),
            visual_direction=idea.creative_direction.visual_direction,
        )

        processing = ScriptProcessing(
            status="draft",
            confidence=idea.processing.confidence,
            processed_at=None,
        )

        return Script(
            schema_version="1.0",
            script_id=script_id,
            created_at=created_at,
            script_version="1",
            source=source,
            target=target,
            metadata=metadata,
            hook=hook,
            introduction=introduction,
            sections=sections,
            conclusion=conclusion,
            cta=cta,
            processing=processing,
        )