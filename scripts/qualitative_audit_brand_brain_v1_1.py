from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

from src.brand_brain import BrandBrainV0
from src.enrichment import SignalEnrichmentEngineV0
from src.radar.models import RadarSignal


PROJECT_ROOT = Path(__file__).resolve().parents[1]

STORE_PATH = (
    PROJECT_ROOT
    / "data"
    / "radar"
    / "futuro_tech_signals.jsonl"
)

OUTPUT_DIR = PROJECT_ROOT / "data" / "audits"

OUTPUT_PATH = (
    OUTPUT_DIR
    / "brand_brain_v1_1_qualitative_audit.csv"
)


BRAND = {
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


TECH_TERMS = (
    "ai",
    "artificial intelligence",
    "chatgpt",
    "gpt",
    "codex",
    "machine learning",
    "deep learning",
    "robot",
    "robotics",
    "gpu",
    "nvidia",
    "software",
    "developer",
    "developers",
    "agent",
    "agents",
    "agentic",
    "technology",
    "hardware",
    "chip",
    "chips",
    "cpu",
    "semiconductor",
    "computer vision",
    "cybersecurity",
    "cyber attack",
    "cyber attack",
)


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
                signals.append(
                    signal_from_dict(json.loads(line))
                )

    return signals


def stable_rank(signal_id: str) -> str:
    """
    Stable deterministic ordering.

    We deliberately avoid random sampling so the audit can be
    reproduced exactly later.
    """

    return hashlib.sha256(
        signal_id.encode("utf-8")
    ).hexdigest()


def has_tech_evidence(signal: RadarSignal) -> bool:
    text = (
        f"{signal.title} "
        f"{signal.summary} "
        f"{' '.join(signal.keywords)} "
        f"{' '.join(signal.topics)}"
    ).lower()

    return any(term in text for term in TECH_TERMS)


def build_evaluations():
    signals = load_signals()

    enrichment = SignalEnrichmentEngineV0()
    brain = BrandBrainV0()

    evaluations = []

    for signal in signals:

        # IMPORTANT:
        # Start from empty enrichment fields.
        #
        # This isolates the Brand Brain + Enrichment behavior
        # instead of allowing previously accumulated taxonomy
        # to influence the audit.
        enriched = enrichment.enrich(
            title=signal.title,
            summary=signal.summary,
            existing_keywords=[],
            existing_topics=[],
        )

        signal.keywords = enriched.keywords
        signal.topics = enriched.topics

        evaluation = brain.evaluate(
            signal,
            BRAND,
        )

        evaluations.append(
            {
                "signal": signal,
                "evaluation": evaluation,
            }
        )

    return evaluations


def select_sample(
    candidates: list[dict],
    size: int,
) -> list[dict]:

    ordered = sorted(
        candidates,
        key=lambda item: stable_rank(
            item["signal"].signal_id
        ),
    )

    return ordered[:size]


def build_strata(evaluations):
    relevant = []
    borderline = []
    filtered_tech = []
    irrelevant = []

    used_ids = set()

    # ---------------------------------------------------------
    # 1. Relevant
    # ---------------------------------------------------------

    relevant_candidates = [
        item
        for item in evaluations
        if item["evaluation"].relevant
    ]

    relevant_sample = select_sample(
        relevant_candidates,
        25,
    )

    for item in relevant_sample:
        used_ids.add(item["signal"].signal_id)

    # ---------------------------------------------------------
    # 2. Borderline
    # ---------------------------------------------------------

    borderline_candidates = [
        item
        for item in evaluations
        if (
            item["signal"].signal_id not in used_ids
            and not item["evaluation"].relevant
            and item["evaluation"].relevance_level
            == "borderline"
        )
    ]

    borderline_sample = select_sample(
        borderline_candidates,
        25,
    )

    for item in borderline_sample:
        used_ids.add(item["signal"].signal_id)

    # ---------------------------------------------------------
    # 3. Filtered but technologically relevant-looking
    # ---------------------------------------------------------

    filtered_tech_candidates = [
        item
        for item in evaluations
        if (
            item["signal"].signal_id not in used_ids
            and not item["evaluation"].relevant
            and has_tech_evidence(item["signal"])
        )
    ]

    filtered_tech_sample = select_sample(
        filtered_tech_candidates,
        25,
    )

    for item in filtered_tech_sample:
        used_ids.add(item["signal"].signal_id)

    # ---------------------------------------------------------
    # 4. Remaining irrelevant
    # ---------------------------------------------------------

    irrelevant_candidates = [
        item
        for item in evaluations
        if (
            item["signal"].signal_id not in used_ids
            and not item["evaluation"].relevant
            and not has_tech_evidence(item["signal"])
        )
    ]

    irrelevant_sample = select_sample(
        irrelevant_candidates,
        25,
    )

    return [
        ("relevant", item)
        for item in relevant_sample
    ] + [
        ("borderline", item)
        for item in borderline_sample
    ] + [
        ("filtered_tech", item)
        for item in filtered_tech_sample
    ] + [
        ("irrelevant", item)
        for item in irrelevant_sample
    ]


def make_row(
    sample_group: str,
    signal: RadarSignal,
    evaluation,
    index: int,
) -> dict:

    return {
        "audit_id": f"audit_{index:03d}",
        "sample_group": sample_group,

        "signal_id": signal.signal_id,
        "title": signal.title,
        "summary": signal.summary,

        "source_type": signal.source_type,
        "platform": signal.platform,
        "published_at": signal.published_at or "",
        "url": signal.url or "",

        "score": evaluation.relevance_score,
        "relevance": evaluation.relevant,
        "relevance_level": evaluation.relevance_level,

        "matched_pillars": " | ".join(
            evaluation.matched_pillars
        ),

        "matched_topics": " | ".join(
            evaluation.matched_topics
        ),

        "rule_flags": " | ".join(
            evaluation.rule_flags
        ),

        "keywords": " | ".join(
            signal.keywords
        ),

        "topics": " | ".join(
            signal.topics
        ),

        # -----------------------------------------------------
        # HUMAN ANNOTATION FIELDS
        # -----------------------------------------------------

        "human_label": "",
        "centrality": "",
        "domain_fit": "",
        "human_notes": "",
    }


def write_csv(rows: list[dict]) -> None:

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    fieldnames = list(rows[0].keys())

    with OUTPUT_PATH.open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(rows)


def print_summary(
    evaluations,
    strata,
    rows,
):

    total = len(evaluations)

    relevant = sum(
        item["evaluation"].relevant
        for item in evaluations
    )

    borderline = sum(
        item["evaluation"].relevance_level
        == "borderline"
        for item in evaluations
    )

    tech_filtered = sum(
        (
            not item["evaluation"].relevant
            and has_tech_evidence(item["signal"])
        )
        for item in evaluations
    )

    print()
    print("=" * 72)
    print(
        "FUTURO TECH — BRAND BRAIN V1.1 "
        "QUALITATIVE AUDIT"
    )
    print("=" * 72)

    print()
    print(f"Store:              {STORE_PATH}")
    print(f"Output:             {OUTPUT_PATH}")
    print()

    print(f"Signals:            {total}")
    print(f"Relevant:           {relevant}")
    print(f"Borderline:         {borderline}")
    print(
        f"Filtered + tech:    {tech_filtered}"
    )

    print()
    print("SAMPLE")
    print("-" * 72)

    counts = {}

    for group, _ in strata:
        counts[group] = counts.get(group, 0) + 1

    for group in (
        "relevant",
        "borderline",
        "filtered_tech",
        "irrelevant",
    ):
        print(
            f"{group:>16}: "
            f"{counts.get(group, 0)}"
        )

    print()
    print(
        f"Rows written:       {len(rows)}"
    )

    print()
    print("HUMAN LABELS")
    print("-" * 72)
    print("A = clearly belongs")
    print("B = potentially belongs")
    print("C = probably does not belong")
    print("D = definitely outside")
    print()
    print("CENTRALITY")
    print("-" * 72)
    print("core      = technology is central")
    print("supporting = technology materially supports story")
    print("incidental = technology is incidental")
    print()
    print(
        "Fill the CSV columns:"
    )
    print(
        "  human_label"
    )
    print(
        "  centrality"
    )
    print(
        "  domain_fit"
    )
    print(
        "  human_notes"
    )
    print()


def main():

    evaluations = build_evaluations()

    strata = build_strata(
        evaluations
    )

    rows = []

    for index, (
        sample_group,
        item,
    ) in enumerate(
        strata,
        start=1,
    ):

        rows.append(
            make_row(
                sample_group=sample_group,
                signal=item["signal"],
                evaluation=item["evaluation"],
                index=index,
            )
        )

    if not rows:
        raise RuntimeError(
            "No audit rows were generated."
        )

    write_csv(rows)

    print_summary(
        evaluations,
        strata,
        rows,
    )


if __name__ == "__main__":
    main()