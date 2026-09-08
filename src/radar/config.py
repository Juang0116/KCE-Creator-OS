from dataclasses import dataclass


@dataclass(frozen=True)
class RSSFeedConfig:
    """
    Configuración de una fuente RSS para Radar.
    """

    name: str
    url: str
    language: str = "es"
    enabled: bool = True