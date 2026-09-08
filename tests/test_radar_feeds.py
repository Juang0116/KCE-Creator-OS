from src.radar.config import RSSFeedConfig
from src.radar.feeds import RSS_FEEDS, TECHCRUNCH_MAIN


def test_techcrunch_feed_config():
    assert isinstance(TECHCRUNCH_MAIN, RSSFeedConfig)

    assert TECHCRUNCH_MAIN.name == "TechCrunch"
    assert TECHCRUNCH_MAIN.url == (
        "https://techcrunch.com/feed/"
    )
    assert TECHCRUNCH_MAIN.language == "en"
    assert TECHCRUNCH_MAIN.enabled is True


def test_rss_feeds_contains_techcrunch():
    assert TECHCRUNCH_MAIN in RSS_FEEDS
    assert len(RSS_FEEDS) == 1