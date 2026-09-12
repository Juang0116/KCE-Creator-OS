from collections import Counter
from pathlib import Path

from src.brand_brain import BrandBrainV0
from src.enrichment import SignalEnrichmentEngineV0
from src.radar.models import RadarSignal


PROJECT_ROOT = Path(__file__).resolve().parents[1]
STORE_PATH = PROJECT_ROOT / "data" / "radar" / "futuro_tech_signals.jsonl"

BRAND = {
    "brand_id": "brand_futuro_tech",
    "identity": {"name": "Futuro Tech"},
    "content": {
        "pillars": ["technology", "AI"],
        "topics": [
            "technology",
            "AI",
            "artificial intelligence",
            "machine learning",
            "software",
            "robotics",
            "future",
            "innovation",
        ],
    },
    "audience": {
        "interests": [
            "technology",
            "AI",
            "artificial intelligence",
            "software",
            "robotics",
            "innovation",
        ],
    },
    "channels": {"primary_platforms": ["YouTube"]},
}


def signal_from_dict(data: dict) -> RadarSignal:
    source = data.get("source", {})
    signal = data.get("signal", {})
    relevance = data.get("relevance", {})
    processing = data.get("processing", {})

    return RadarSignal(
        signal_id=data["signal_id"],
        detected_at=data["detected_at"],
        radar_version=data["radar_version"],
        source_type=source.get("type", ""),
        platform=source.get("platform", ""),
        url=source.get("url"),
        author=source.get("author"),
        published_at=source.get("published_at"),
        title=signal.get("title", ""),
        summary=signal.get("summary", ""),
        # Intentionally start clean. Enrichment is the variable under audit.
        keywords=[],
        topics=[],
        language=signal.get("language", "en"),
        evidence=data.get("evidence", {}),
        niches=relevance.get("niches", []),
        relevance_reason=relevance.get("relevance_reason", ""),
        status=processing.get("status", "detected"),
        confidence=processing.get("confidence", 0.0),
        processed_at=processing.get("processed_at"),
    )


def load_signals() -> list[RadarSignal]:
    signals = []
    with STORE_PATH.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                signals.append(signal_from_dict(__import__("json").loads(line)))
    return signals


def main() -> None:
    signals = load_signals()
    enrichment = SignalEnrichmentEngineV0()
    brain = BrandBrainV0()

    evaluations = []

    for signal in signals:
        enriched = enrichment.enrich(
            title=signal.title,
            summary=signal.summary,
            existing_keywords=[],
            existing_topics=[],
        )
        signal.keywords = enriched.keywords
        signal.topics = enriched.topics

        evaluation = brain.evaluate(signal, BRAND)
        evaluations.append((signal, evaluation))

    total = len(evaluations)
    relevant = sum(e.relevant for _, e in evaluations)
    borderline = sum(e.relevance_level == "borderline" for _, e in evaluations)
    highly_relevant = sum(
        e.relevance_level == "highly_relevant" for _, e in evaluations
    )
    irrelevant = total - relevant

    recommendations = Counter()
    scores = Counter()
    specific = 0
    generic_only = 0
    generic_filtered = 0

    for signal, evaluation in evaluations:
        # Opportunity Engine is intentionally not run here: this is a
        # Brand Brain audit, so we isolate Brand Brain behavior.
        if evaluation.relevant:
            recommendations["relevant"] += 1
        else:
            recommendations["filtered"] += 1

        bucket = (
            "80-100" if evaluation.relevance_score >= 80
            else "70-79" if evaluation.relevance_score >= 70
            else "60-69" if evaluation.relevance_score >= 60
            else "50-59" if evaluation.relevance_score >= 50
            else "40-49" if evaluation.relevance_score >= 40
            else "0-39"
        )
        scores[bucket] += 1

        if "no_specific_topic_evidence" not in evaluation.rule_flags:
            specific += 1
        if "generic_ai_evidence" in evaluation.rule_flags:
            generic_only += 1
            if not evaluation.relevant:
                generic_filtered += 1

    print()
    print("=" * 72)
    print("FUTURO TECH — BRAND BRAIN V1.1 AUDIT")
    print("=" * 72)
    print(f"Store: {STORE_PATH}")
    print()
    print(f"Signals:          {total}")
    print(f"Relevant:         {relevant}")
    print(f"Highly relevant:  {highly_relevant}")
    print(f"Borderline:       {borderline}")
    print(f"Irrelevant:       {irrelevant}")
    print()
    print("EVIDENCE")
    print(f"Specific evidence: {specific}")
    print(f"Generic AI-only:   {generic_only}")
    print(f"Generic AI filtered: {generic_filtered}")
    print()
    print("SCORE DISTRIBUTION")
    for bucket in ("80-100", "70-79", "60-69", "50-59", "40-49", "0-39"):
        print(f"{bucket:>7}: {scores[bucket]}")
    print()
    print("TOP 25 RELEVANT SIGNALS BY BRAND SCORE")
    print("-" * 72)

    top = sorted(
        (
            (signal, evaluation)
            for signal, evaluation in evaluations
            if evaluation.relevant
        ),
        key=lambda item: item[1].relevance_score,
        reverse=True,
    )

    for index, (signal, evaluation) in enumerate(top[:25], 1):
        print(
            f"{index:02d}. {evaluation.relevance_score:5.1f} | "
            f"{evaluation.relevance_level:16} | "
            f"{signal.title}"
        )
        print(
            f"    pillars={evaluation.matched_pillars} "
            f"topics={evaluation.matched_topics} "
            f"flags={evaluation.rule_flags}"
        )

    print()
    print("TOP 25 FILTERED SIGNALS WITH AI/TECH EVIDENCE")
    print("-" * 72)

    tech_terms = (
        "ai",
        "artificial intelligence",
        "chatgpt",
        "gpt",
        "codex",
        "machine learning",
        "robot",
        "robotics",
        "gpu",
        "nvidia",
        "software",
        "developer",
        "agent",
        "agentic",
        "technology",
    )

    filtered = []
    for signal, evaluation in evaluations:
        text = f"{signal.title} {signal.summary}".lower()
        if not evaluation.relevant and any(term in text for term in tech_terms):
            filtered.append((signal, evaluation))

    filtered.sort(key=lambda item: item[1].relevance_score, reverse=True)

    for index, (signal, evaluation) in enumerate(filtered[:25], 1):
        print(
            f"{index:02d}. {evaluation.relevance_score:5.1f} | "
            f"{evaluation.relevance_level:16} | "
            f"{signal.title}"
        )
        print(
            f"    topics={signal.topics} "
            f"flags={evaluation.rule_flags}"
        )


if __name__ == "__main__":
    main()
