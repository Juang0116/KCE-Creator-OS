from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class Event:
    event_id: str
    created_at: str
    event_type: str
    entity_type: str
    entity_id: str
    payload: dict[str, Any] = field(
        default_factory=dict
    )

    @classmethod
    def create(
        cls,
        event_id: str,
        event_type: str,
        entity_type: str,
        entity_id: str,
        payload: dict[str, Any] | None = None,
    ) -> "Event":
        return cls(
            event_id=event_id,
            created_at=datetime.now(
                timezone.utc
            ).isoformat(),
            event_type=event_type,
            entity_type=entity_type,
            entity_id=entity_id,
            payload=payload or {},
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "created_at": self.created_at,
            "event_type": self.event_type,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "payload": self.payload,
        }