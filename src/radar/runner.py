from src.enrichment import SignalEnrichmentEngineV0
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
    Signal Enrichment V0
        ↓
    enriched raw signals
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
        enrichment: SignalEnrichmentEngineV0 | None = None,
    ):
        self.feeds = feeds
        self.radar = radar or RadarV0()
        self.deduplicator = deduplicator
        self.enrichment = enrichment or SignalEnrichmentEngineV0()

    def run(self):
        """
        Ejecuta todas las fuentes habilitadas.

        El enriquecimiento ocurre sobre los raw signals
        antes de convertirlos en RadarSignal.

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

        enriched_raw_signals = [
            self._enrich_signal(raw_signal)
            for raw_signal in all_raw_signals
        ]

        signals = self.radar.collect(enriched_raw_signals)

        if self.deduplicator is not None:
            signals = self.deduplicator.filter_new(signals)

        return signals

    def _enrich_signal(self, raw_signal: dict) -> dict:
        """
        Enriquece un raw signal sin modificar el objeto original.

        El resultado mantiene todos los campos originales
        y sustituye únicamente keywords/topics por sus
        versiones enriquecidas.
        """

        result = self.enrichment.enrich(
            title=raw_signal.get("title", ""),
            summary=raw_signal.get("summary", ""),
            existing_keywords=raw_signal.get("keywords", []),
            existing_topics=raw_signal.get("topics", []),
        )

        enriched_signal = dict(raw_signal)

        enriched_signal["keywords"] = result.keywords
        enriched_signal["topics"] = result.topics

        return enriched_signal