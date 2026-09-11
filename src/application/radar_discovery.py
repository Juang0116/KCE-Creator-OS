from __future__ import annotations

from src.orchestration import DiscoveryPackage
from src.radar import RadarV0

from .discovery_facade import DiscoveryFacadeV0


class RadarDiscoveryApplicationServiceV0:
    """
    Application service que conecta Radar V0 con Discovery.

    Flujo:

        raw signals
            -> RadarV0
            -> RadarSignal
            -> DiscoveryFacadeV0
            -> DiscoveryPackage

    Este servicio no contiene lógica de dominio.
    Su responsabilidad es coordinar ambos módulos.
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
        raw_signals: list[dict],
        brand: dict,
    ) -> list[DiscoveryPackage]:
        signals = self.radar.collect(raw_signals)

        packages = []

        for signal in signals:
            package = self.discovery.run(
                signal=signal,
                brand=brand,
            )

            packages.append(package)

        return packages