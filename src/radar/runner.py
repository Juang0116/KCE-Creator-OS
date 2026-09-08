from src.radar.config import RSSFeedConfig
from src.radar.radar import RadarV0
from src.radar.sources.rss import RSSSource


class RadarRunner:
    """
    Orquestador V0 del Radar.

    Flujo:
    RSS_FEEDS
        ↓
    feeds habilitados
        ↓
    RSSSource
        ↓
    raw signals
        ↓
    RadarV0
        ↓
    RadarSignal[]
    """

    def __init__(
        self,
        feeds: list[RSSFeedConfig],
        radar: RadarV0 | None = None,
    ):
        self.feeds = feeds
        self.radar = radar or RadarV0()

    def run(self):
        """
        Ejecuta todas las fuentes habilitadas
        y devuelve señales normalizadas.
        """

        all_raw_signals = []

        for feed_config in self.feeds:
            if not feed_config.enabled:
                continue

            source = RSSSource(feed_config)
            raw_signals = source.fetch()

            all_raw_signals.extend(raw_signals)

        return self.radar.collect(all_raw_signals)