from src.radar.config import RSSFeedConfig


def test_rss_feed_config_defaults():
    feed = RSSFeedConfig(
        name="KCE Test Feed",
        url="https://example.com/feed.xml",
    )

    assert feed.name == "KCE Test Feed"
    assert feed.url == "https://example.com/feed.xml"
    assert feed.language == "es"
    assert feed.enabled is True


def test_rss_feed_config_supports_custom_values():
    feed = RSSFeedConfig(
        name="Tech Feed",
        url="https://example.com/tech.xml",
        language="en",
        enabled=False,
    )

    assert feed.name == "Tech Feed"
    assert feed.url == "https://example.com/tech.xml"
    assert feed.language == "en"
    assert feed.enabled is False