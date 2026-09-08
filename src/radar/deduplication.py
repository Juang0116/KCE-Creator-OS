import hashlib
import json

from src.radar.models import RadarSignal


class RadarDeduplicator:
    """
    Deduplicación determinista V0 para señales del Radar.

    Reglas:
    - Si existe URL, la URL identifica la señal.
    - Si no existe URL, se utiliza un fingerprint determinista.
    - No modifica ni elimina señales del historial.
    """

    def __init__(self, existing_signals: list[dict] | None = None):
        self._seen_keys: set[str] = set()

        for signal in existing_signals or []:
            self._seen_keys.add(self.key_from_dict(signal))

    def is_duplicate(self, signal: RadarSignal) -> bool:
        """
        Devuelve True si la señal ya fue vista.
        """

        return self.key(signal) in self._seen_keys

    def register(self, signal: RadarSignal) -> None:
        """
        Registra una señal como vista.
        """

        self._seen_keys.add(self.key(signal))

    def filter_new(
        self,
        signals: list[RadarSignal],
    ) -> list[RadarSignal]:
        """
        Devuelve únicamente señales nuevas.

        Las señales aceptadas quedan registradas inmediatamente
        para evitar duplicados dentro del mismo lote.
        """

        new_signals = []

        for signal in signals:
            if self.is_duplicate(signal):
                continue

            self.register(signal)
            new_signals.append(signal)

        return new_signals

    @staticmethod
    def key(signal: RadarSignal) -> str:
        """
        Genera una clave determinista para un RadarSignal.
        """

        if signal.url:
            return f"url:{signal.url.strip()}"

        fingerprint_data = {
            "title": signal.title.strip(),
            "summary": signal.summary.strip(),
            "author": (signal.author or "").strip(),
            "published_at": (signal.published_at or "").strip(),
        }

        payload = json.dumps(
            fingerprint_data,
            ensure_ascii=False,
            sort_keys=True,
        )

        digest = hashlib.sha256(
            payload.encode("utf-8")
        ).hexdigest()

        return f"fingerprint:{digest}"

    @staticmethod
    def key_from_dict(signal: dict) -> str:
        """
        Genera la misma clave a partir de una señal
        previamente persistida como diccionario.
        """

        source = signal.get("source", {})
        signal_data = signal.get("signal", {})

        url = source.get("url")

        if url:
            return f"url:{url.strip()}"

        fingerprint_data = {
            "title": signal_data.get("title", "").strip(),
            "summary": signal_data.get("summary", "").strip(),
            "author": (source.get("author") or "").strip(),
            "published_at": (
                source.get("published_at") or ""
            ).strip(),
        }

        payload = json.dumps(
            fingerprint_data,
            ensure_ascii=False,
            sort_keys=True,
        )

        digest = hashlib.sha256(
            payload.encode("utf-8")
        ).hexdigest()

        return f"fingerprint:{digest}"