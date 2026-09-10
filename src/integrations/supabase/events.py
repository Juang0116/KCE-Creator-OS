from __future__ import annotations

from typing import Any

from supabase import Client

from src.events import Event


class SupabaseEventRepository:
    """
    Supabase-backed repository for Event objects.

    V0 persists events directly into creator_os.events.
    """

    TABLE_NAME = "events"

    def __init__(self, client: Client) -> None:
        self.client = client

    def _table(self) -> Any:
        return (
            self.client
            .schema("creator_os")
            .table(self.TABLE_NAME)
        )

    def save(self, event: Event) -> Event:
        if not event.event_id:
            raise ValueError(
                "Event ID must not be empty."
            )

        (
            self._table()
            .upsert(
                event.to_dict(),
                on_conflict="event_id",
            )
            .execute()
        )

        return event

    def get(
        self,
        event_id: str,
    ) -> Event | None:
        if not event_id:
            raise ValueError(
                "Event ID must not be empty."
            )

        response = (
            self._table()
            .select("*")
            .eq(
                "event_id",
                event_id,
            )
            .limit(1)
            .execute()
        )

        if not response.data:
            return None

        return Event(
            event_id=response.data[0]["event_id"],
            created_at=response.data[0]["created_at"],
            event_type=response.data[0]["event_type"],
            entity_type=response.data[0]["entity_type"],
            entity_id=response.data[0]["entity_id"],
            payload=response.data[0].get(
                "payload",
                {},
            ),
        )

    def exists(
        self,
        event_id: str,
    ) -> bool:
        if not event_id:
            raise ValueError(
                "Event ID must not be empty."
            )

        response = (
            self._table()
            .select("event_id")
            .eq(
                "event_id",
                event_id,
            )
            .limit(1)
            .execute()
        )

        return bool(response.data)

    def delete(
        self,
        event_id: str,
    ) -> bool:
        if not event_id:
            raise ValueError(
                "Event ID must not be empty."
            )

        response = (
            self._table()
            .delete()
            .eq(
                "event_id",
                event_id,
            )
            .execute()
        )

        return bool(response.data)

    def list_all(self) -> list[Event]:
        response = (
            self._table()
            .select("*")
            .execute()
        )

        return [
            Event(
                event_id=row["event_id"],
                created_at=row["created_at"],
                event_type=row["event_type"],
                entity_type=row["entity_type"],
                entity_id=row["entity_id"],
                payload=row.get(
                    "payload",
                    {},
                ),
            )
            for row in response.data
        ]