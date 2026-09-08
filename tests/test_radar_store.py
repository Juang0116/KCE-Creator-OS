from src.radar.models import RadarSignal
from src.radar.store import RadarStore


def make_signal(signal_id: str) -> RadarSignal:
    return RadarSignal(
        signal_id=signal_id,
        detected_at="2026-09-08T00:00:00+00:00",
        radar_version="0.1.0",
        source_type="rss",
        platform="rss",
        url="https://example.com/article",
        author="KCE Test",
        published_at="2026-09-08T00:00:00+00:00",
        title=f"Test signal {signal_id}",
        summary="Test summary",
        keywords=["test"],
        topics=["technology"],
        language="en",
        evidence={},
        niches=[],
        relevance_reason="",
        status="detected",
        confidence=0.5,
        processed_at=None,
    )


def test_radar_store_saves_and_loads_signals(tmp_path):
    store = RadarStore(tmp_path / "signals.jsonl")

    signals = [
        make_signal("sig_001"),
        make_signal("sig_002"),
    ]

    store.save(signals)

    loaded = store.load()

    assert len(loaded) == 2
    assert loaded[0]["signal_id"] == "sig_001"
    assert loaded[1]["signal_id"] == "sig_002"


def test_radar_store_creates_parent_directory(tmp_path):
    store = RadarStore(
        tmp_path / "radar" / "signals.jsonl"
    )

    signal = make_signal("sig_001")

    store.save([signal])

    assert store.path.exists()
    assert len(store.load()) == 1


def test_radar_store_empty_file_returns_empty_list(tmp_path):
    store = RadarStore(tmp_path / "signals.jsonl")

    assert store.load() == []