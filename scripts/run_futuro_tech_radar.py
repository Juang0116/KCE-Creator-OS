import argparse
from collections import Counter
from pathlib import Path

from src.brand_brain import BrandBrainV0
from src.discovery import DiscoveryEngineV0
from src.enrichment import SignalEnrichmentEngineV0
from src.opportunity import OpportunityEngineV0
from src.orchestration import DiscoveryWorkflowV0
from src.radar.futuro_tech import FUTURO_TECH_FEEDS
from src.radar.models import RadarSignal
from src.radar.pipeline import RadarPipeline
from src.radar.store import RadarStore


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data" / "radar"

FUTURO_TECH_STORE_PATH = (
    DATA_DIR / "futuro_tech_signals.jsonl"
)


FUTURO_TECH_BRAND = {
    "brand_id": "brand_futuro_tech",
    "identity": {
        "name": "Futuro Tech",
    },
    "content": {
        "pillars": [
            "technology",
            "AI",
        ],
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
    "channels": {
        "primary_platforms": [
            "YouTube",
        ],
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the Futuro Tech Radar and Discovery workflow."
    )

    parser.add_argument(
        "--replay",
        action="store_true",
        help="Replay all persisted Radar signals from the local JSONL store.",
    )

    parser.add_argument(
        "--reenrich",
        action="store_true",
        help=(
            "Re-enrich replayed Radar signals in memory "
            "before running Discovery."
        ),
    )

    return parser.parse_args()


def print_header(title: str) -> None:
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def print_feed_configuration() -> None:
    print_header("FUTURO TECH — FEED CONFIGURATION")

    for feed in FUTURO_TECH_FEEDS:
        status = "ENABLED" if feed.enabled else "DISABLED"

        print(f"{feed.name}")
        print(f"  URL: {feed.url}")
        print(f"  Language: {feed.language}")
        print(f"  Status: {status}")
        print()


def radar_signal_from_dict(data: dict) -> RadarSignal:
    """
    Reconstruct a RadarSignal from its persisted dictionary representation.
    """

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
        keywords=signal.get("keywords", []),
        topics=signal.get("topics", []),
        language=signal.get("language", "es"),
        evidence=data.get("evidence", {}),
        niches=relevance.get("niches", []),
        relevance_reason=relevance.get(
            "relevance_reason",
            "",
        ),
        status=processing.get(
            "status",
            "detected",
        ),
        confidence=processing.get(
            "confidence",
            0.0,
        ),
        processed_at=processing.get(
            "processed_at",
        ),
    )


def load_replay_signals(store: RadarStore) -> list[RadarSignal]:
    raw_signals = store.load()

    return [
        radar_signal_from_dict(data)
        for data in raw_signals
    ]


def re_enrich_signals(
    signals: list[RadarSignal],
) -> list[RadarSignal]:
    """
    Re-enrich persisted Radar signals in memory.

    This does not modify the persisted JSONL store.
    """

    enrichment = SignalEnrichmentEngineV0()

    enriched_signals = []

    for signal in signals:
        result = enrichment.enrich(
            title=signal.title,
            summary=signal.summary,
            existing_keywords=signal.keywords,
            existing_topics=signal.topics,
        )

        signal.keywords = result.keywords
        signal.topics = result.topics

        enriched_signals.append(signal)

    return enriched_signals


def build_score_bucket(score: float) -> str:
    """
    Return a human-readable score bucket.
    """

    if score >= 80:
        return "80–100"
    if score >= 70:
        return "70–79"
    if score >= 60:
        return "60–69"
    if score >= 50:
        return "50–59"
    if score >= 40:
        return "40–49"

    return "0–39"


def print_discovery_statistics(
    valid_packages: list,
) -> None:
    """
    Print statistical information about generated opportunities.

    This is observability only. It does not alter scoring or filtering.
    """

    recommendation_counts = Counter()
    score_buckets = Counter()
    pillar_counts = Counter()
    topic_counts = Counter()

    for package in valid_packages:
        discovery = package.discovery
        opportunity = discovery.opportunity
        brand_evaluation = discovery.brand_evaluation

        recommendation = opportunity.analysis.recommendation

        recommendation_counts[recommendation] += 1

        score = opportunity.scoring.total_score
        score_buckets[build_score_bucket(score)] += 1

        for pillar in brand_evaluation.matched_pillars:
            pillar_counts[pillar] += 1

        for topic in brand_evaluation.matched_topics:
            topic_counts[topic] += 1

    print_header("DISCOVERY STATISTICS")

    print("RECOMMENDATIONS")
    print(
        f"  strong_candidate: "
        f"{recommendation_counts.get('strong_candidate', 0)}"
    )
    print(
        f"  candidate: "
        f"{recommendation_counts.get('candidate', 0)}"
    )
    print(
        f"  weak_candidate: "
        f"{recommendation_counts.get('weak_candidate', 0)}"
    )
    print(
        f"  reject: "
        f"{recommendation_counts.get('reject', 0)}"
    )

    print()
    print("SCORE DISTRIBUTION")

    for bucket in (
        "80–100",
        "70–79",
        "60–69",
        "50–59",
        "40–49",
        "0–39",
    ):
        print(
            f"  {bucket}: "
            f"{score_buckets.get(bucket, 0)}"
        )

    print()
    print("MATCHED PILLARS")

    if pillar_counts:
        for pillar, count in pillar_counts.most_common():
            print(
                f"  {pillar}: {count}"
            )
    else:
        print("  None")

    print()
    print("MATCHED TOPICS")

    if topic_counts:
        for topic, count in topic_counts.most_common():
            print(
                f"  {topic}: {count}"
            )
    else:
        print("  None")


def run_discovery(
    signals: list[RadarSignal],
) -> None:
    brand_brain = BrandBrainV0()

    opportunity_engine = OpportunityEngineV0()

    discovery_engine = DiscoveryEngineV0(
        brand_brain=brand_brain,
        opportunity_engine=opportunity_engine,
    )

    discovery_workflow = DiscoveryWorkflowV0(
        discovery_engine=discovery_engine,
    )

    print_header("DISCOVERY EXECUTION")

    packages = []

    for signal in signals:
        package = discovery_workflow.run(
            signal=signal,
            brand=FUTURO_TECH_BRAND,
        )

        packages.append(package)

    valid_packages = [
        package
        for package in packages
        if package.discovery.idea is not None
    ]

    filtered_packages = [
        package
        for package in packages
        if package.discovery.idea is None
    ]

    print(f"Signals processed: {len(packages)}")
    print(f"Content opportunities: {len(valid_packages)}")
    print(f"Filtered: {len(filtered_packages)}")

    print_discovery_statistics(
        valid_packages=valid_packages,
    )

    ranked_packages = sorted(
        valid_packages,
        key=lambda package: (
            package.discovery.opportunity.scoring.total_score
        ),
        reverse=True,
    )

    print_header("TOP FUTURO TECH OPPORTUNITIES")

    if not ranked_packages:
        print("No content opportunities generated.")
        print()
        print(
            "This is useful information: "
            "the current Brand Brain may be too strict "
            "for the vocabulary used by real RSS sources."
        )
        return

    for index, package in enumerate(
        ranked_packages[:10],
        start=1,
    ):
        discovery = package.discovery
        opportunity = discovery.opportunity
        idea = discovery.idea

        print()
        print(f"{index}. {idea.concept}")

        print(
            f"   Score: "
            f"{opportunity.scoring.total_score:.2f}/100"
        )

        print(
            f"   Recommendation: "
            f"{opportunity.analysis.recommendation}"
        )

        print(
            f"   Signal: "
            f"{discovery.signal.title}"
        )

        print(
            f"   Source: "
            f"{discovery.signal.source_type}"
        )

        if discovery.brand_evaluation.matched_pillars:
            print(
                "   Matched pillars: "
                + ", ".join(
                    discovery.brand_evaluation.matched_pillars
                )
            )

        if discovery.brand_evaluation.matched_topics:
            print(
                "   Matched topics: "
                + ", ".join(
                    discovery.brand_evaluation.matched_topics
                )
            )

        if package.approval is not None:
            print(
                f"   Approval: "
                f"{package.approval.decision.status}"
            )

    print_header("EXECUTION SUMMARY")

    print(f"Stored signals: {len(signals)}")
    print(f"Opportunities: {len(valid_packages)}")
    print(f"Filtered: {len(filtered_packages)}")

    print()
    print("Radar execution completed successfully.")
    print()
    print(
        "Next step: inspect the real opportunities "
        "before changing the scoring system."
    )


def main() -> None:
    args = parse_args()

    print_header("KCE CREATOR OS — FUTURO TECH RADAR V0")

    print_feed_configuration()

    store = RadarStore(
        path=FUTURO_TECH_STORE_PATH,
    )

    if args.reenrich and not args.replay:
        print()
        print(
            "Error: --reenrich requires --replay."
        )
        print(
            "Use: python -m scripts.run_futuro_tech_radar "
            "--replay --reenrich"
        )
        return

    if args.replay:
        print_header("RADAR REPLAY")

        print(
            f"Loading persisted signals from:\n"
            f"{FUTURO_TECH_STORE_PATH}"
        )

        signals = load_replay_signals(store)

        print()
        print(
            f"Signals loaded from store: "
            f"{len(signals)}"
        )

        if args.reenrich:
            print_header("SIGNAL RE-ENRICHMENT")

            print(
                "Re-enriching persisted signals in memory..."
            )

            signals = re_enrich_signals(signals)

            print(
                f"Signals re-enriched: "
                f"{len(signals)}"
            )

            print(
                "Persisted JSONL store was not modified."
            )

    else:
        print_header("RADAR EXECUTION")

        print(f"Store: {FUTURO_TECH_STORE_PATH}")
        print()
        print("Collecting real RSS signals...")

        pipeline = RadarPipeline(
            feeds=FUTURO_TECH_FEEDS,
            store=store,
        )

        signals = pipeline.run()

        print()
        print(
            f"New signals collected: "
            f"{len(signals)}"
        )

        if not signals:
            print()
            print("No new signals were collected.")
            print()
            print("This can mean:")
            print(
                "  • the feeds returned no new entries"
            )
            print(
                "  • the signals were already stored"
            )
            print(
                "  • a source returned no usable items"
            )
            print()
            return

    run_discovery(signals)


if __name__ == "__main__":
    main()