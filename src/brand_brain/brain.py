from src.radar import RadarSignal

from .models import BrandEvaluation


class BrandBrainV0:
    """
    Brand Brain V0:
    Evalúa qué tan relevante es una señal para una marca.

    Esta versión es determinista y no utiliza IA externa.
    """

    def evaluate(
        self,
        signal: RadarSignal,
        brand: dict,
    ) -> BrandEvaluation:
        brand_id = brand["brand_id"]

        content = brand.get("content", {})
        pillars = content.get("pillars", [])
        topics = content.get("topics", [])

        signal_topics = signal.topics
        signal_keywords = signal.keywords

        matched_pillars = self._match_terms(
            signal_topics + signal_keywords,
            pillars,
        )

        matched_topics = self._match_terms(
            signal_topics + signal_keywords,
            topics,
        )

        relevance_score = self._calculate_score(
            matched_pillars,
            matched_topics,
        )

        relevant = relevance_score > 0

        reason = self._build_reason(
            relevant,
            matched_pillars,
            matched_topics,
        )

        confidence = self._calculate_confidence(
            matched_pillars,
            matched_topics,
        )

        return BrandEvaluation(
            brand_id=brand_id,
            signal_id=signal.signal_id,
            relevant=relevant,
            relevance_score=relevance_score,
            matched_pillars=matched_pillars,
            matched_topics=matched_topics,
            reason=reason,
            rule_flags=[],
            confidence=confidence,
        )

    @staticmethod
    def _match_terms(
        signal_terms: list[str],
        brand_terms: list[str],
    ) -> list[str]:
        """
        Encuentra coincidencias entre términos de la señal
        y términos definidos por la marca.
        """

        signal_normalized = {
            term.strip().lower()
            for term in signal_terms
            if term
        }

        matches = []

        for brand_term in brand_terms:
            if not isinstance(brand_term, str):
                continue

            normalized = brand_term.strip().lower()

            if normalized in signal_normalized:
                matches.append(brand_term)

        return matches

    @staticmethod
    def _calculate_score(
        matched_pillars: list[str],
        matched_topics: list[str],
    ) -> float:
        """
        Calcula relevancia V0 en escala 0–10.

        Los pilares tienen mayor peso que los topics.
        """

        score = (
            len(matched_pillars) * 2.5
            + len(matched_topics) * 1.5
        )

        return min(score, 10.0)

    @staticmethod
    def _calculate_confidence(
        matched_pillars: list[str],
        matched_topics: list[str],
    ) -> float:
        """
        Estima la confianza del matching.
        """

        matches = len(matched_pillars) + len(matched_topics)

        if matches == 0:
            return 0.2

        if matches == 1:
            return 0.6

        if matches == 2:
            return 0.8

        return 0.95

    @staticmethod
    def _build_reason(
        relevant: bool,
        matched_pillars: list[str],
        matched_topics: list[str],
    ) -> str:
        if not relevant:
            return (
                "La señal no presenta coincidencias suficientes "
                "con los temas o pilares de la marca."
            )

        parts = []

        if matched_pillars:
            parts.append(
                "pilares: " + ", ".join(matched_pillars)
            )

        if matched_topics:
            parts.append(
                "topics: " + ", ".join(matched_topics)
            )

        return (
            "La señal presenta coincidencias con "
            + " y ".join(parts)
            + "."
        )