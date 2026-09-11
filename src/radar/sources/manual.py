from __future__ import annotations


class ManualRadarSource:
    """
    Simple in-memory Radar source.

    Used for:
    - local development
    - tests
    - controlled experiments
    - initial Content Engine prototyping

    It does not normalize signals.
    """

    def __init__(
        self,
        raw_signals: list[dict] | None = None,
    ) -> None:
        self.raw_signals = raw_signals or []

    def fetch(self) -> list[dict]:
        return list(self.raw_signals)
    