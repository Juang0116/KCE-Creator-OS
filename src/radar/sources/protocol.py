from __future__ import annotations

from typing import Protocol


class RadarSource(Protocol):
    """
    Contract for a Radar source.

    A source is responsible only for obtaining
    raw signals. Normalization into RadarSignal
    remains the responsibility of RadarV0.
    """

    def fetch(self) -> list[dict]:
        ...