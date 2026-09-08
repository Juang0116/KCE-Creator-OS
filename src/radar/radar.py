from datetime import datetime, timezone
from uuid import uuid4

from .models import RadarSignal


class RadarV0:
    """
    Radar V0:
    Convierte señales crudas en objetos RadarSignal.

    En esta primera versión no consulta APIs externas.
    """


    def __init__(self, radar_version: str = "0.1.0"):
        self.radar_version = radar_version


    def collect(self, raw_signals: list[dict]) -> list[RadarSignal]:
        """
        Recibe una lista de señales crudas y devuelve
        una lista de RadarSignal normalizados.
        """

        signals = []

        for raw_signal in raw_signals:
            signal = self._normalize_signal(raw_signal)
            signals.append(signal)

        return signals


    def _normalize_signal(self, raw_signal: dict) -> RadarSignal:
        """
        Convierte una señal cruda individual en RadarSignal.
        """

        detected_at = datetime.now(timezone.utc).isoformat()

        return RadarSignal(
            signal_id=f"sig_{uuid4().hex[:12]}",
            detected_at=detected_at,
            radar_version=self.radar_version,

            source_type=raw_signal.get("source_type", "other"),
            platform=raw_signal.get("platform", "unknown"),
            url=raw_signal.get("url"),
            author=raw_signal.get("author"),
            published_at=raw_signal.get("published_at"),

            title=raw_signal["title"],
            summary=raw_signal["summary"],
            keywords=raw_signal.get("keywords", []),
            topics=raw_signal.get("topics", []),
            language=raw_signal.get("language", "es"),

            niches=raw_signal.get("niches", []),
            relevance_reason=raw_signal.get(
                "relevance_reason",
                ""
            ),

            status="detected",
            confidence=raw_signal.get("confidence", 0.5),
            processed_at=None,
        )