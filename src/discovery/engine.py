from datetime import datetime, timezone
from uuid import uuid4

from src.brand_brain import BrandBrainV0
from src.content.ideas import ContentIdeaEngineV0
from src.opportunity import OpportunityEngineV0
from src.radar import RadarSignal

from .models import (
    DiscoveryProcessing,
    DiscoveryResult,
)


class DiscoveryEngineV0:
    """
    Discovery Engine V0.

    Orquesta:

    RadarSignal
        -> Brand Brain
        -> Opportunity
        -> Content Idea

    Discovery aplica el filtro de relevancia
    de marca antes de generar una ContentIdea.

    No utiliza IA externa,
    no publica contenido
    y no interactúa con servicios externos.
    """

    def __init__(
        self,
        brand_brain=None,
        opportunity_engine=None,
        content_idea_engine=None,
    ):
        self.brand_brain = (
            brand_brain
            or BrandBrainV0()
        )

        self.opportunity_engine = (
            opportunity_engine
            or OpportunityEngineV0()
        )

        self.content_idea_engine = (
            content_idea_engine
            or ContentIdeaEngineV0()
        )

    def run(
        self,
        signal: RadarSignal,
        brand: dict,
    ) -> DiscoveryResult:
        brand_evaluation = (
            self.brand_brain.evaluate(
                signal,
                brand,
            )
        )

        opportunity = (
            self.opportunity_engine.evaluate(
                signal=signal,
                brand=brand,
                brand_evaluation=brand_evaluation,
            )
        )

        recommendation = (
            opportunity.analysis.recommendation
        )

        should_generate_idea = (
            brand_evaluation.relevant
            and recommendation != "reject"
        )

        idea = None

        if should_generate_idea:
            idea = (
                self.content_idea_engine.generate(
                    opportunity=opportunity,
                    brand=brand,
                )
            )

        confidence_values = [
            brand_evaluation.confidence,
            opportunity.processing.confidence,
        ]

        if idea is not None:
            confidence_values.append(
                idea.processing.confidence
            )

        confidence = min(confidence_values)

        is_filtered = (
            not brand_evaluation.relevant
            or recommendation == "reject"
        )

        processing_status = (
            "filtered"
            if is_filtered
            else "draft"
        )

        processing = DiscoveryProcessing(
            status=processing_status,
            confidence=confidence,
            processed_at=datetime.now(
                timezone.utc
            ).isoformat(),
        )

        return DiscoveryResult(
            discovery_id=(
                f"discovery_{uuid4().hex[:12]}"
            ),
            created_at=datetime.now(
                timezone.utc
            ).isoformat(),
            discovery_version="0.1.0",
            signal=signal,
            brand_evaluation=brand_evaluation,
            opportunity=opportunity,
            idea=idea,
            processing=processing,
        )