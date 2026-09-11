from __future__ import annotations

from src.orchestration import DiscoveryPackage
from src.radar import RadarV0, RadarSource

from .discovery_facade import DiscoveryFacadeV0


class RadarDiscoveryApplicationServiceV0:
    """
    Application service that connects a RadarSource with Discovery.

    RadarSource
        -> RadarV0
        -> RadarSignal
        -> DiscoveryFacadeV0
        -> DiscoveryPackage
    """

    def __init__(
        self,
        radar: RadarV0,
        discovery: DiscoveryFacadeV0,
    ) -> None:
        self.radar = radar
        self.discovery = discovery

    def run(
        self,
        source: RadarSource,
        brand: dict,
    ) -> list[DiscoveryPackage]:
        raw_signals = source.fetch()
        signals = self.radar.collect(raw_signals)

        packages: list[DiscoveryPackage] = []

        for signal in signals:
            package = self.discovery.run(
                signal=signal,
                brand=brand,
            )
            packages.append(package)

        return packages