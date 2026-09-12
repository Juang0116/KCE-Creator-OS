from src.enrichment import SignalEnrichmentEngineV0
from src.radar.config import RSSFeedConfig
from src.radar.runner import RadarRunner


class FakeRSSSource:
    def __init__(self, feed_config):
        self.feed_config = feed_config

    def fetch(self):
        return [
            {
                "source_type": "rss",
                "platform": "rss",
                "url": "https://example.com/article",
                "author": None,
                "published_at": None,
                "title": "NVIDIA launches new AI chips",
                "summary": (
                    "The company announced new GPU technology "
                    "for artificial intelligence workloads."
                ),
                "keywords": ["Product"],
                "topics": ["Product"],
                "language": "en",
                "evidence": {},
                "niches": [],
                "relevance_reason": "",
                "confidence": 0.5,
            }
        ]


class FakeRadar:
    def __init__(self):
        self.received_raw_signals = None

    def collect(self, raw_signals):
        self.received_raw_signals = raw_signals
        return raw_signals


def test_runner_enriches_raw_signals_before_radar(monkeypatch):
    monkeypatch.setattr(
        "src.radar.runner.RSSSource",
        FakeRSSSource,
    )

    radar = FakeRadar()

    runner = RadarRunner(
        feeds=[
            RSSFeedConfig(
                name="Test Feed",
                url="https://example.com/feed.xml",
                language="en",
                enabled=True,
            )
        ],
        radar=radar,
        enrichment=SignalEnrichmentEngineV0(),
    )

    result = runner.run()

    assert len(result) == 1

    enriched_signal = radar.received_raw_signals[0]

    assert "Product" in enriched_signal["keywords"]
    assert "NVIDIA" in enriched_signal["keywords"]
    assert "AI" in enriched_signal["keywords"]
    assert "GPU" in enriched_signal["keywords"]

    assert "Product" in enriched_signal["topics"]
    assert "AI" in enriched_signal["topics"]
    assert "chips" in enriched_signal["topics"]


def test_runner_preserves_original_raw_signal_fields(monkeypatch):
    monkeypatch.setattr(
        "src.radar.runner.RSSSource",
        FakeRSSSource,
    )

    radar = FakeRadar()

    runner = RadarRunner(
        feeds=[
            RSSFeedConfig(
                name="Test Feed",
                url="https://example.com/feed.xml",
                language="en",
                enabled=True,
            )
        ],
        radar=radar,
    )

    runner.run()

    signal = radar.received_raw_signals[0]

    assert signal["source_type"] == "rss"
    assert signal["platform"] == "rss"
    assert signal["url"] == "https://example.com/article"
    assert signal["title"] == "NVIDIA launches new AI chips"
    assert signal["language"] == "en"
    assert signal["confidence"] == 0.5


def test_runner_skips_disabled_feeds(monkeypatch):
    class FailingRSSSource:
        def __init__(self, feed_config):
            raise AssertionError(
                "Disabled feeds must not instantiate RSSSource."
            )

    monkeypatch.setattr(
        "src.radar.runner.RSSSource",
        FailingRSSSource,
    )

    radar = FakeRadar()

    runner = RadarRunner(
        feeds=[
            RSSFeedConfig(
                name="Disabled Feed",
                url="https://example.com/feed.xml",
                language="en",
                enabled=False,
            )
        ],
        radar=radar,
    )

    result = runner.run()

    assert result == []
    assert radar.received_raw_signals == []