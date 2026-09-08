import json
from pathlib import Path

from src.radar.models import RadarSignal


class RadarStore:
    """
    Persistencia local V0 para señales del Radar.

    Responsabilidad única:
    - guardar RadarSignal como JSONL;
    - leer señales persistidas.

    No descarga feeds.
    No normaliza señales.
    No calcula relevancia.
    No calcula Opportunity Score.
    """

    def __init__(self, path: str | Path):
        self.path = Path(path)

    def save(self, signals: list[RadarSignal]) -> None:
        """
        Añade señales al archivo JSONL.
        """

        self.path.parent.mkdir(parents=True, exist_ok=True)

        with self.path.open("a", encoding="utf-8") as file:
            for signal in signals:
                file.write(
                    json.dumps(
                        signal.to_dict(),
                        ensure_ascii=False,
                    )
                    + "\n"
                )

    def load(self) -> list[dict]:
        """
        Lee todas las señales persistidas.

        Devuelve diccionarios JSON para mantener
        el Store independiente del modelo RadarSignal.
        """

        if not self.path.exists():
            return []

        signals = []

        with self.path.open("r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if not line:
                    continue

                signals.append(json.loads(line))

        return signals