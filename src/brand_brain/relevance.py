from dataclasses import dataclass

from src.radar.models import RadarSignal


@dataclass(frozen=True)
class RelevanceResult:
    """
    Resultado determinista de relevancia de una señal
    respecto a un Brand DNA.
    """

    score: float
    matched_keywords: list[str]
    matched_topics: list[str]
    reasons: list[str]

    @property
    def level(self) -> str:
        if self.score >= 0.75:
            return "high"

        if self.score >= 0.50:
            return "medium"

        return "low"


class RelevanceEngine:
    """
    Relevance Engine V0.

    Compara una RadarSignal con el Brand DNA canónico.

    V0 utiliza únicamente señales explícitas del Brand DNA:
    - market.category
    - audience.interests
    - audience.problems
    - audience.desires
    - content.pillars
    - content.topics

    No utiliza LLM.
    No genera contenido.
    No calcula Opportunity Score.
    """

    def evaluate(
        self,
        signal: RadarSignal,
        brand_dna: dict,
    ) -> RelevanceResult:
        market = brand_dna.get("market", {})
        audience = brand_dna.get("audience", {})
        content = brand_dna.get("content", {})

        brand_keywords = self._normalize_list(
            [market.get("category", "")]
            + audience.get("interests", [])
            + audience.get("problems", [])
            + audience.get("desires", [])
        )

        brand_topics = self._normalize_list(
            content.get("pillars", [])
            + content.get("topics", [])
        )

        signal_keywords = self._normalize_list(
            signal.keywords
        )

        signal_topics = self._normalize_list(
            signal.topics
        )

        matched_keywords = sorted(
            set(signal_keywords) & set(brand_keywords)
        )

        matched_topics = sorted(
            set(signal_topics) & set(brand_topics)
        )

        keyword_score = (
            min(len(matched_keywords) / 3, 1.0)
            if brand_keywords
            else 0.0
        )

        topic_score = (
            min(len(matched_topics) / 2, 1.0)
            if brand_topics
            else 0.0
        )

        score = (
            (keyword_score * 0.4)
            + (topic_score * 0.6)
        )

        reasons = []

        if matched_keywords:
            reasons.append(
                "Matched Brand DNA keywords: "
                + ", ".join(matched_keywords)
            )

        if matched_topics:
            reasons.append(
                "Matched Brand DNA topics: "
                + ", ".join(matched_topics)
            )

        if not reasons:
            reasons.append(
                "No relevant Brand DNA matches found."
            )

        return RelevanceResult(
            score=round(score, 4),
            matched_keywords=matched_keywords,
            matched_topics=matched_topics,
            reasons=reasons,
        )

    @staticmethod
    def _normalize_list(
        values: list[str],
    ) -> list[str]:
        return sorted(
            {
                value.strip().lower()
                for value in values
                if value and value.strip()
            }
        )