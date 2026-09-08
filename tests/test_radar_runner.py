from src.radar.config import RSSFeedConfig
from src.radar.deduplication import RadarDeduplicator
from src.radar.radar import RadarV0
from src.radar.runner import RadarRunner


class FakeRSSSource:
    def __init__(self, feed_config):
        self.feed_config = feed_config

    def fetch(self):
        return [
            {
                "source_type": "rss",
                "platform": "rss",
                "url": self.feed_config.url,
                "author": None,
                "published_at": None,
                "title": f"Signal from {self.feed_config.name}",
                "summary": "Test signal",
                "keywords": [],
                "topics": [],
                "language": self.feed_config.language,
                "evidence": {},
                "niches": [],
                "relevance_reason": "",
                "confidence": 0.5,
            }
        ]


def test_radar_runner_processes_enabled_feeds(monkeypatch):
    feeds = [
        RSSFeedConfig(
            name="Enabled Feed",
            url="https://example.com/enabled.xml",
            language="en",
            enabled=True,
        ),
        RSSFeedConfig(
            name="Disabled Feed",
            url="https://example.com/disabled.xml",
            language="en",
            enabled=False,
        ),
    ]

    monkeypatch.setattr(
        "src.radar.runner.RSSSource",
        FakeRSSSource,
    )

    runner = RadarRunner(
        feeds=feeds,
        radar=RadarV0(),
    )

    signals = runner.run()

    assert len(signals) == 1
    assert signals[0].title == "Signal from Enabled Feed"
    assert signals[0].url == "https://example.com/enabled.xml"


def test_radar_runner_filters_duplicate_signals(monkeypatch):
    feeds = [
        RSSFeedConfig(
            name="Test Feed",
            url="https://example.com/feed.xml",
            language="en",
            enabled=True,
        ),
    ]

    monkeypatch.setattr(
        "src.radar.runner.RSSSource",
        FakeRSSSource,
    )

    deduplicator = RadarDeduplicator()

    runner = RadarRunner(
        feeds=feeds,
        radar=RadarV0(),
        deduplicator=deduplicator,
    )

    first_run = runner.run()
    second_run = runner.run()

    assert len(first_run) == 1
    assert len(second_run) == 0