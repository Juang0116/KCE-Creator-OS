from src.radar.config import RSSFeedConfig


FUTURO_TECH_FEEDS = [
    RSSFeedConfig(
        name="OpenAI News",
        url="https://openai.com/news/rss.xml",
        language="en",
        enabled=True,
    ),
    RSSFeedConfig(
        name="Google DeepMind",
        url="https://deepmind.google/blog/rss.xml",
        language="en",
        enabled=True,
    ),
    RSSFeedConfig(
        name="Hugging Face Blog",
        url="https://huggingface.co/blog/feed.xml",
        language="en",
        enabled=True,
    ),
    RSSFeedConfig(
        name="NVIDIA Blog",
        url="https://blogs.nvidia.com/feed/",
        language="en",
        enabled=True,
    ),
]