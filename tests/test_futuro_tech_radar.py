from src.radar.config import RSSFeedConfig
from src.radar.futuro_tech import FUTURO_TECH_FEEDS


def test_futuro_tech_has_rss_feeds():
    assert FUTURO_TECH_FEEDS
    assert all(
        isinstance(feed, RSSFeedConfig)
        for feed in FUTURO_TECH_FEEDS
    )


def test_futuro_tech_feeds_are_enabled():
    assert all(
        feed.enabled
        for feed in FUTURO_TECH_FEEDS
    )


def test_futuro_tech_feed_names_are_unique():
    names = [
        feed.name
        for feed in FUTURO_TECH_FEEDS
    ]

    assert len(names) == len(set(names))


def test_futuro_tech_feed_urls_are_unique():
    urls = [
        feed.url
        for feed in FUTURO_TECH_FEEDS
    ]

    assert len(urls) == len(set(urls))


def test_futuro_tech_uses_english_sources():
    assert all(
        feed.language == "en"
        for feed in FUTURO_TECH_FEEDS
    )


def test_futuro_tech_contains_core_ai_sources():
    names = {
        feed.name
        for feed in FUTURO_TECH_FEEDS
    }

    assert "OpenAI News" in names
    assert "Google DeepMind" in names
    assert "Hugging Face Blog" in names
    assert "NVIDIA Blog" in names