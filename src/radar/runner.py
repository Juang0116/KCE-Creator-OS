from src.radar.config import RSSFeedConfig
from src.radar.deduplication import RadarDeduplicator
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
        ↓
    optional deduplication
        ↓
    new RadarSignal[]
    """

    def __init__(
        self,
        feeds: list[RSSFeedConfig],
        radar: RadarV0 | None = None,
        deduplicator: RadarDeduplicator | None = None,
    ):
        self.feeds = feeds
        self.radar = radar or RadarV0()
        self.deduplicator = deduplicator

    def run(self):
        """
        Ejecuta todas las fuentes habilitadas.

        Si existe un deduplicador, devuelve únicamente
        señales nuevas.
        """

        all_raw_signals = []

        for feed_config in self.feeds:
            if not feed_config.enabled:
                continue

            source = RSSSource(feed_config)
            raw_signals = source.fetch()

            all_raw_signals.extend(raw_signals)

        signals = self.radar.collect(all_raw_signals)

        if self.deduplicator is not None:
            signals = self.deduplicator.filter_new(signals)

        return signals