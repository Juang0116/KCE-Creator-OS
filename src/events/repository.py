from __future__ import annotations

from .models import Event


class EventRepository:
    """In-memory repository for Event objects."""

    def __init__(self) -> None:
        self._events: dict[str, Event] = {}

    def save(self, event: Event) -> Event:
        if not event.event_id:
            raise ValueError("Event ID must not be empty.")

        self._events[event.event_id] = event
        return event

    def get(self, event_id: str) -> Event | None:
        if not event_id:
            raise ValueError("Event ID must not be empty.")

        return self._events.get(event_id)

    def exists(self, event_id: str) -> bool:
        if not event_id:
            raise ValueError("Event ID must not be empty.")

        return event_id in self._events

    def delete(self, event_id: str) -> bool:
        if not event_id:
            raise ValueError("Event ID must not be empty.")

        if event_id not in self._events:
            return False

        del self._events[event_id]
        return True

    def list_all(self) -> list[Event]:
        return list(self._events.values())