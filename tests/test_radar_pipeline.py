from src.radar.config import RSSFeedConfig
from src.radar.pipeline import RadarPipeline
from src.radar.store import RadarStore


def test_pipeline_persists_new_signals_and_remembers_them(
    tmp_path,
    monkeypatch,
):
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
                    "title": "Persistent test signal",
                    "summary": "Test summary",
                    "keywords": [],
                    "topics": [],
                    "language": self.feed_config.language,
                    "evidence": {},
                    "niches": [],
                    "relevance_reason": "",
                    "confidence": 0.5,
                }
            ]

    monkeypatch.setattr(
        "src.radar.runner.RSSSource",
        FakeRSSSource,
    )

    store_path = tmp_path / "radar" / "signals.jsonl"

    feeds = [
        RSSFeedConfig(
            name="Persistent Test Feed",
            url="https://example.com/feed.xml",
            language="en",
            enabled=True,
        )
    ]

    first_pipeline = RadarPipeline(
        feeds=feeds,
        store=RadarStore(store_path),
    )

    first_run = first_pipeline.run()

    assert len(first_run) == 1
    assert len(RadarStore(store_path).load()) == 1

    second_pipeline = RadarPipeline(
        feeds=feeds,
        store=RadarStore(store_path),
    )

    second_run = second_pipeline.run()

    assert second_run == []
    assert len(RadarStore(store_path).load()) == 1