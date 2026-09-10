from __future__ import annotations

from src.events import Event
from src.persistence import MemoryRepository, Repository


class EventRepository:
    """
    Repository specialized for Event objects.

    V0 uses the existing generic Repository abstraction
    with an in-memory implementation.
    """

    def __init__(
        self,
        repository: Repository[Event] | None = None,
    ) -> None:
        self.repository = (
            repository
            if repository is not None
            else MemoryRepository[Event]()
        )

    def save(self, event: Event) -> Event:
        if not event.event_id:
            raise ValueError(
                "Event ID must not be empty."
            )

        return self.repository.save(
            event.event_id,
            event,
        )

    def get(
        self,
        event_id: str,
    ) -> Event | None:
        if not event_id:
            raise ValueError(
                "Event ID must not be empty."
            )

        return self.repository.get(event_id)

    def exists(
        self,
        event_id: str,
    ) -> bool:
        if not event_id:
            raise ValueError(
                "Event ID must not be empty."
            )

        return self.repository.exists(event_id)

    def delete(
        self,
        event_id: str,
    ) -> bool:
        if not event_id:
            raise ValueError(
                "Event ID must not be empty."
            )

        return self.repository.delete(event_id)

    def list_all(self) -> list[Event]:
        return self.repository.list_all()