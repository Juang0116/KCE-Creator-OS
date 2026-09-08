from src.radar.deduplication import RadarDeduplicator
from src.radar.models import RadarSignal
from src.radar.store import RadarStore


def make_signal(
    signal_id: str,
    url: str,
) -> RadarSignal:
    return RadarSignal(
        signal_id=signal_id,
        detected_at="2026-09-08T00:00:00+00:00",
        radar_version="0.1.0",
        source_type="rss",
        platform="rss",
        url=url,
        author="KCE Test",
        published_at="2026-09-08T00:00:00+00:00",
        title=f"Signal {signal_id}",
        summary="Test summary",
        keywords=[],
        topics=["technology"],
        language="en",
        evidence={},
        niches=[],
        relevance_reason="",
        status="detected",
        confidence=0.5,
        processed_at=None,
    )


def test_deduplication_works_with_persisted_store(tmp_path):
    store = RadarStore(
        tmp_path / "radar" / "signals.jsonl"
    )

    existing = make_signal(
        "sig_existing",
        "https://example.com/existing",
    )

    store.save([existing])

    persisted = store.load()

    deduplicator = RadarDeduplicator(
        existing_signals=persisted
    )

    signals = [
        make_signal(
            "sig_duplicate",
            "https://example.com/existing",
        ),
        make_signal(
            "sig_new",
            "https://example.com/new",
        ),
    ]

    new_signals = deduplicator.filter_new(signals)

    assert len(new_signals) == 1
    assert new_signals[0].signal_id == "sig_new"

    store.save(new_signals)

    final_signals = store.load()

    assert len(final_signals) == 2

    final_ids = {
        signal["signal_id"]
        for signal in final_signals
    }

    assert final_ids == {
        "sig_existing",
        "sig_new",
    }