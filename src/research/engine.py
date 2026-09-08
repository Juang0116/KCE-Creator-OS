from datetime import datetime, timezone
from uuid import uuid4

from src.content.ideas import ContentIdea
from .models import (
    ResearchBrief,
    ResearchObjective,
    ResearchProcessing,
    ResearchScope,
)


class ResearchEngineV0:
    def generate(
        self,
        content_idea: ContentIdea,
        brand: dict,
    ) -> ResearchBrief:
        objective = self._build_objective(content_idea)
        scope = self._build_scope(content_idea, brand)

        processing = ResearchProcessing(
            status="draft",
            confidence=self._calculate_confidence(content_idea),
            processed_at=datetime.now(timezone.utc).isoformat(),
        )

        return ResearchBrief(
            research_id=f"research_{uuid4().hex[:12]}",
            created_at=datetime.now(timezone.utc).isoformat(),
            research_version="0.1.0",
            idea_id=content_idea.idea_id,
            opportunity_id=content_idea.opportunity_id,
            signal_id=content_idea.signal_id,
            brand_id=content_idea.brand_id,
            channel=content_idea.channel,
            platform=content_idea.platform,
            objective=objective,
            scope=scope,
            findings=[],
            sources=[],
            research_gaps=[],
            processing=processing,
        )

    @staticmethod
    def _build_objective(
        content_idea: ContentIdea,
    ) -> ResearchObjective:
        concept = content_idea.concept

        research_question = (
            f"¿Qué necesitamos saber para explicar correctamente "
            f"'{concept.working_title}'?"
        )

        content_goal = concept.core_promise

        key_questions = [
            f"¿Qué evidencia respalda la afirmación principal de "
            f"'{concept.working_title}'?",
            "¿Cuáles son los datos y hechos más relevantes?",
            "¿Qué contexto necesita la audiencia para entender el tema?",
            "¿Qué afirmaciones requieren verificación adicional?",
        ]

        return ResearchObjective(
            research_question=research_question,
            content_goal=content_goal,
            key_questions=key_questions,
        )

    @staticmethod
    def _build_scope(
        content_idea: ContentIdea,
        brand: dict,
    ) -> ResearchScope:
        content = brand.get("content", {})

        topics = list(
            dict.fromkeys(
                [
                    content_idea.concept.content_pillar,
                    *content.get("topics", []),
                ]
            )
        )

        keywords = list(
            dict.fromkeys(
                [
                    content_idea.concept.working_title,
                    *content.get("topics", []),
                ]
            )
        )

        exclusions = [
            "Información no relacionada con el objetivo del contenido.",
            "Afirmaciones sin fuente verificable.",
        ]

        return ResearchScope(
            topics=topics,
            keywords=keywords,
            exclusions=exclusions,
        )

    @staticmethod
    def _calculate_confidence(
        content_idea: ContentIdea,
    ) -> float:
        return min(
            max(content_idea.processing.confidence, 0.0),
            1.0,
        )