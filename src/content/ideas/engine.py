from datetime import datetime, timezone
from uuid import uuid4

from src.opportunity import Opportunity

from .models import (
    ContentAudience,
    ContentConcept,
    ContentIdea,
    ContentProcessing,
    ContentProduction,
    CreativeDirection,
)


class ContentIdeaEngineV0:
    """
    Content Idea Engine V0:
    Convierte una oportunidad evaluada en una idea
    concreta de contenido.

    En esta primera versión utiliza reglas deterministas.
    No consulta modelos de IA externos.
    """

    def generate(
        self,
        opportunity: Opportunity,
        brand: dict,
    ) -> ContentIdea:
        concept = self._build_concept(
            opportunity,
            brand,
        )

        audience = self._build_audience(brand)

        creative_direction = self._build_creative_direction(
            opportunity,
            brand,
        )

        production = self._build_production(
            opportunity,
        )

        processing = ContentProcessing(
            status="draft",
            confidence=self._calculate_confidence(
                opportunity
            ),
            processed_at=datetime.now(
                timezone.utc
            ).isoformat(),
        )

        return ContentIdea(
            idea_id=f"idea_{uuid4().hex[:12]}",
            created_at=datetime.now(
                timezone.utc
            ).isoformat(),
            idea_version="0.1.0",
            opportunity_id=opportunity.opportunity_id,
            signal_id=opportunity.signal_id,
            brand_id=opportunity.brand_id,
            channel=opportunity.channel,
            platform=self._get_platform(brand),
            concept=concept,
            audience=audience,
            creative_direction=creative_direction,
            production=production,
            processing=processing,
        )

    @staticmethod
    def _build_concept(
        opportunity: Opportunity,
        brand: dict,
    ) -> ContentConcept:
        title = opportunity.analysis.why_now

        pillar = "General"

        if opportunity.scoring.relevance > 0:
            matched_pillars = brand.get(
                "content",
                {},
            ).get("pillars", [])

            if matched_pillars:
                pillar = matched_pillars[0]

        return ContentConcept(
            working_title=title,
            hook=(
                "Hay una señal que está generando interés "
                "y merece una explicación."
            ),
            core_promise=(
                "Explicar por qué esta oportunidad "
                "es relevante para la audiencia."
            ),
            angle=opportunity.analysis.why_this_brand,
            format="explainer",
            estimated_duration_seconds=600,
            content_pillar=pillar,
        )

    @staticmethod
    def _build_audience(
        brand: dict,
    ) -> ContentAudience:
        audience = brand.get(
            "audience",
            {},
        )

        target = audience.get(
            "target",
            "Audiencia general interesada en el tema.",
        )

        interests = audience.get(
            "interests",
            [],
        )

        if interests:
            audience_need = (
                "Entender mejor "
                + ", ".join(interests[:3])
                + "."
            )
        else:
            audience_need = (
                "Entender el tema de forma clara."
            )

        return ContentAudience(
            target=target,
            audience_need=audience_need,
            expected_value=(
                "Información clara, contexto y una "
                "explicación útil sobre el tema."
            ),
        )

    @staticmethod
    def _build_creative_direction(
        opportunity: Opportunity,
        brand: dict,
    ) -> CreativeDirection:
        return CreativeDirection(
            storytelling_approach=(
                "Presentar el contexto, explicar "
                "el problema y desarrollar la oportunidad "
                "hasta una conclusión clara."
            ),
            visual_direction=(
                "Utilizar gráficos, capturas, imágenes "
                "de apoyo y elementos visuales relacionados "
                "con el tema."
            ),
            voice_direction=(
                "Claro, informativo y alineado con "
                "la personalidad de la marca."
            ),
            key_elements=[
                "context",
                "evidence",
                "explanation",
                "conclusion",
            ],
        )

    @staticmethod
    def _build_production(
        opportunity: Opportunity,
    ) -> ContentProduction:
        if opportunity.scoring.production_feasibility >= 8:
            complexity = "low"
            hours = 3.0
        elif opportunity.scoring.production_feasibility >= 6:
            complexity = "medium"
            hours = 5.0
        else:
            complexity = "high"
            hours = 8.0

        return ContentProduction(
            complexity=complexity,
            estimated_production_hours=hours,
            required_assets=[
                "research_sources",
                "visual_references",
                "thumbnail",
            ],
            ai_assistance=[
                "research",
                "drafting",
                "visual_asset_generation",
            ],
        )

    @staticmethod
    def _calculate_confidence(
        opportunity: Opportunity,
    ) -> float:
        confidence = opportunity.processing.confidence

        if opportunity.scoring.total_score >= 80:
            confidence += 0.05

        return min(confidence, 1.0)

    @staticmethod
    def _get_platform(
        brand: dict,
    ) -> str:
        platforms = brand.get(
            "channels_community",
            {},
        ).get(
            "primary_platforms",
            [],
        )

        if platforms:
            return platforms[0]

        return "YouTube"