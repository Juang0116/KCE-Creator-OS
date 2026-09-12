from datetime import datetime, timezone
from uuid import uuid4

from src.brand_brain import BrandEvaluation
from src.radar import RadarSignal

from .models import (
    Opportunity,
    OpportunityAnalysis,
    OpportunityProcessing,
    OpportunityScoring,
)


class OpportunityEngineV0:
    def evaluate(
        self,
        signal: RadarSignal,
        brand: dict,
        brand_evaluation: BrandEvaluation,
    ) -> Opportunity:
        scoring = self._calculate_scoring(
            signal,
            brand,
            brand_evaluation,
        )

        recommendation = self._get_recommendation(
            scoring.total_score
        )

        analysis = OpportunityAnalysis(
            why_now=self._build_why_now(signal),
            why_this_brand=self._build_why_this_brand(
                brand_evaluation
            ),
            risks=[],
            recommendation=recommendation,
        )

        processing = OpportunityProcessing(
            status="evaluated",
            confidence=brand_evaluation.confidence,
            processed_at=datetime.now(timezone.utc).isoformat(),
        )

        return Opportunity(
            opportunity_id=f"opp_{uuid4().hex[:12]}",
            created_at=datetime.now(timezone.utc).isoformat(),
            opportunity_version="0.1.0",
            signal_id=signal.signal_id,
            brand_id=brand["brand_id"],
            channel=self._get_channel(brand),
            scoring=scoring,
            analysis=analysis,
            processing=processing,
        )

    def _calculate_scoring(
        self,
        signal: RadarSignal,
        brand: dict,
        brand_evaluation: BrandEvaluation,
    ) -> OpportunityScoring:
        # Brand Brain relevance is 0-100.
        # Opportunity scoring dimensions are 0-10.
        relevance = min(
            max(brand_evaluation.relevance_score / 10.0, 0.0),
            10.0,
        )

        audience_fit = self._calculate_audience_fit(
            signal,
            brand,
        )

        trend_strength = self._calculate_trend_strength(
            signal
        )

        novelty = self._calculate_novelty(
            signal
        )

        production_feasibility = (
            self._calculate_production_feasibility(
                signal,
                brand,
            )
        )

        evergreen_potential = (
            self._calculate_evergreen_potential(
                signal
            )
        )

        total_score = (
            relevance
            + audience_fit
            + trend_strength
            + novelty
            + production_feasibility
            + evergreen_potential
        ) / 60 * 100

        return OpportunityScoring(
            relevance=round(relevance, 2),
            audience_fit=audience_fit,
            trend_strength=trend_strength,
            novelty=novelty,
            production_feasibility=production_feasibility,
            evergreen_potential=evergreen_potential,
            total_score=round(total_score, 2),
        )

    @staticmethod
    def _calculate_audience_fit(
        signal: RadarSignal,
        brand: dict,
    ) -> float:
        audience = brand.get("audience", {})

        interests = audience.get("interests", [])

        if not interests:
            return 5.0

        signal_terms = {
            term.strip().lower()
            for term in signal.topics + signal.keywords
            if term
        }

        matches = sum(
            1
            for interest in interests
            if isinstance(interest, str)
            and interest.strip().lower() in signal_terms
        )

        return min(5.0 + matches * 2.0, 10.0)

    @staticmethod
    def _calculate_trend_strength(
        signal: RadarSignal,
    ) -> float:
        engagement = signal.evidence.get(
            "engagement",
            {},
        )

        views = engagement.get("views")
        likes = engagement.get("likes")
        comments = engagement.get("comments")
        shares = engagement.get("shares")

        values = [
            value
            for value in (
                views,
                likes,
                comments,
                shares,
            )
            if isinstance(value, (int, float))
        ]

        if not values:
            return 5.0

        total_engagement = sum(values)

        if total_engagement >= 1_000_000:
            return 10.0

        if total_engagement >= 100_000:
            return 8.0

        if total_engagement >= 10_000:
            return 6.5

        if total_engagement >= 1_000:
            return 5.0

        return 3.5

    @staticmethod
    def _calculate_novelty(
        signal: RadarSignal,
    ) -> float:
        observations = signal.evidence.get(
            "observations",
            [],
        )

        if observations:
            return 7.0

        return 5.0

    @staticmethod
    def _calculate_production_feasibility(
        signal: RadarSignal,
        brand: dict,
    ) -> float:
        source_type = signal.source_type.lower()

        if source_type in {
            "rss",
            "news",
            "forum",
        }:
            return 8.0

        if source_type in {
            "social",
            "search",
        }:
            return 7.0

        if source_type == "video":
            return 6.0

        return 5.0

    @staticmethod
    def _calculate_evergreen_potential(
        signal: RadarSignal,
    ) -> float:
        topics = {
            topic.strip().lower()
            for topic in signal.topics
            if topic
        }

        evergreen_terms = {
            "technology",
            "ai",
            "education",
            "history",
            "tutorial",
            "guide",
            "language",
        }

        if topics.intersection(evergreen_terms):
            return 8.0

        return 5.0

    @staticmethod
    def _get_recommendation(
        total_score: float,
    ) -> str:
        if total_score >= 80:
            return "strong_candidate"

        if total_score >= 60:
            return "candidate"

        if total_score >= 40:
            return "weak_candidate"

        return "reject"

    @staticmethod
    def _build_why_now(
        signal: RadarSignal,
    ) -> str:
        return (
            f"La señal detectada indica actividad relevante "
            f"alrededor de '{signal.title}'."
        )

    @staticmethod
    def _build_why_this_brand(
        evaluation: BrandEvaluation,
    ) -> str:
        if evaluation.matched_pillars:
            pillars = ", ".join(
                evaluation.matched_pillars
            )

            return (
                f"La oportunidad encaja con los pilares de la marca: "
                f"{pillars}."
            )

        return (
            "La oportunidad presenta una coincidencia general "
            "con la marca."
        )

    @staticmethod
    def _get_channel(
        brand: dict,
    ) -> str:
        channels = brand.get(
            "channels_community",
            {},
        )

        primary_platforms = channels.get(
            "primary_platforms",
            [],
        )

        if primary_platforms:
            return primary_platforms[0]

        return "unknown"