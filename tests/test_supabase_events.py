from unittest.mock import Mock

import pytest

from src.events import Event
from src.integrations.supabase.events import (
    SupabaseEventRepository,
)


def make_client() -> Mock:
    client = Mock()

    schema = client.schema.return_value

    table = Mock()

    response = Mock()
    response.data = []

    table.upsert.return_value.execute.return_value = response
    table.select.return_value.eq.return_value.limit.return_value.execute.return_value = response
    table.select.return_value.execute.return_value = response
    table.delete.return_value.eq.return_value.execute.return_value = response

    schema.table.return_value = table

    return client


def make_event(
    event_id: str = "event_001",
) -> Event:
    return Event(
        event_id=event_id,
        created_at="2026-09-10T00:00:00+00:00",
        event_type="discovery.created",
        entity_type="discovery",
        entity_id="discovery_001",
        payload={
            "source": "test",
        },
    )


def test_save_event() -> None:
    client = make_client()

    repository = SupabaseEventRepository(client)
    event = make_event()

    repository.save(event)

    table = (
        client
        .schema("creator_os")
        .table("events")
    )

    table.upsert.assert_called_once_with(
        event.to_dict(),
        on_conflict="event_id",
    )


def test_get_event() -> None:
    client = make_client()

    event = make_event()

    response = Mock()
    response.data = [event.to_dict()]

    table = (
        client
        .schema("creator_os")
        .table("events")
    )

    table.select.return_value.eq.return_value.limit.return_value.execute.return_value = response

    repository = SupabaseEventRepository(client)

    restored = repository.get("event_001")

    assert restored == event


def test_get_missing_event() -> None:
    client = make_client()

    repository = SupabaseEventRepository(client)

    assert repository.get("missing") is None


def test_exists_event() -> None:
    client = make_client()

    response = Mock()
    response.data = [
        {
            "event_id": "event_001",
        }
    ]

    table = (
        client
        .schema("creator_os")
        .table("events")
    )

    table.select.return_value.eq.return_value.limit.return_value.execute.return_value = response

    repository = SupabaseEventRepository(client)

    assert repository.exists("event_001") is True


def test_delete_event() -> None:
    client = make_client()

    response = Mock()
    response.data = [
        {
            "event_id": "event_001",
        }
    ]

    table = (
        client
        .schema("creator_os")
        .table("events")
    )

    table.delete.return_value.eq.return_value.execute.return_value = response

    repository = SupabaseEventRepository(client)

    assert repository.delete("event_001") is True


def test_list_all_events() -> None:
    client = make_client()

    event_001 = make_event("event_001")
    event_002 = make_event("event_002")

    response = Mock()
    response.data = [
        event_001.to_dict(),
        event_002.to_dict(),
    ]

    table = (
        client
        .schema("creator_os")
        .table("events")
    )

    table.select.return_value.execute.return_value = response

    repository = SupabaseEventRepository(client)

    events = repository.list_all()

    assert events == [
        event_001,
        event_002,
    ]


def test_empty_event_id_is_rejected() -> None:
    client = make_client()

    repository = SupabaseEventRepository(client)

    with pytest.raises(ValueError):
        repository.save(make_event(""))

    with pytest.raises(ValueError):
        repository.get("")

    with pytest.raises(ValueError):
        repository.exists("")

    with pytest.raises(ValueError):
        repository.delete("")