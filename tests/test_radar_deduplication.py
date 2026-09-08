from src.radar.deduplication import RadarDeduplicator
from src.radar.models import RadarSignal


def make_signal(
    signal_id: str,
    url: str | None = "https://example.com/article",
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
        title="Test signal",
        summary="Test summary",
        keywords=[],
        topics=[],
        language="en",
        evidence={},
        niches=[],
        relevance_reason="",
        status="detected",
        confidence=0.5,
        processed_at=None,
    )


def test_duplicate_is_detected_by_url():
    first = make_signal("sig_001")
    second = make_signal("sig_002")

    deduplicator = RadarDeduplicator()

    deduplicator.register(first)

    assert deduplicator.is_duplicate(second) is True


def test_different_urls_are_not_duplicates():
    first = make_signal(
        "sig_001",
        "https://example.com/article-1",
    )
    second = make_signal(
        "sig_002",
        "https://example.com/article-2",
    )

    deduplicator = RadarDeduplicator()

    deduplicator.register(first)

    assert deduplicator.is_duplicate(second) is False


def test_duplicate_without_url_uses_fingerprint():
    first = make_signal("sig_001", url=None)
    second = make_signal("sig_002", url=None)

    deduplicator = RadarDeduplicator()

    deduplicator.register(first)

    assert deduplicator.is_duplicate(second) is True


def test_filter_new_removes_duplicates_inside_same_batch():
    first = make_signal("sig_001")
    duplicate = make_signal("sig_002")
    unique = make_signal(
        "sig_003",
        "https://example.com/other",
    )

    deduplicator = RadarDeduplicator()

    new_signals = deduplicator.filter_new(
        [first, duplicate, unique]
    )

    assert len(new_signals) == 2
    assert new_signals[0].signal_id == "sig_001"
    assert new_signals[1].signal_id == "sig_003"


def test_existing_persisted_signals_are_detected():
    existing = make_signal("sig_old")

    deduplicator = RadarDeduplicator(
        existing_signals=[existing.to_dict()]
    )

    new_signal = make_signal("sig_new")

    assert deduplicator.is_duplicate(new_signal) is True