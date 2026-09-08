from src.radar.config import RSSFeedConfig


TECHCRUNCH_MAIN = RSSFeedConfig(
    name="TechCrunch",
    url="https://techcrunch.com/feed/",
    language="en",
    enabled=True,
)


RSS_FEEDS = [
    TECHCRUNCH_MAIN,
]