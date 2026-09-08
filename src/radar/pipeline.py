from src.radar.config import RSSFeedConfig
from src.radar.deduplication import RadarDeduplicator
from src.radar.radar import RadarV0
from src.radar.runner import RadarRunner
from src.radar.store import RadarStore


class RadarPipeline:
    """
    Pipeline operativo V0 del Radar.

    Flujo:

    Store
        ↓
    historial existente
        ↓
    Deduplicator
        ↓
    RadarRunner
        ↓
    nuevas señales
        ↓
    Store
    """

    def __init__(
        self,
        feeds: list[RSSFeedConfig],
        store: RadarStore,
        radar: RadarV0 | None = None,
    ):
        self.store = store
        self.radar = radar or RadarV0()

        existing_signals = self.store.load()

        self.deduplicator = RadarDeduplicator(
            existing_signals=existing_signals,
        )

        self.runner = RadarRunner(
            feeds=feeds,
            radar=self.radar,
            deduplicator=self.deduplicator,
        )

    def run(self):
        """
        Ejecuta el Radar y persiste únicamente señales nuevas.
        """

        new_signals = self.runner.run()

        if new_signals:
            self.store.save(new_signals)

        return new_signals