import pytest

from src.events import Event, EventRepository


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


def test_save_and_get_event() -> None:
    repository = EventRepository()

    event = make_event()

    saved = repository.save(event)
    restored = repository.get("event_001")

    assert saved == event
    assert restored == event


def test_exists_event() -> None:
    repository = EventRepository()

    event = make_event()

    assert repository.exists("event_001") is False

    repository.save(event)

    assert repository.exists("event_001") is True


def test_list_all_events() -> None:
    repository = EventRepository()

    event_001 = make_event("event_001")
    event_002 = make_event("event_002")

    repository.save(event_001)
    repository.save(event_002)

    events = repository.list_all()

    assert len(events) == 2
    assert event_001 in events
    assert event_002 in events


def test_delete_event() -> None:
    repository = EventRepository()

    repository.save(make_event())

    assert repository.delete("event_001") is True
    assert repository.get("event_001") is None
    assert repository.exists("event_001") is False


def test_delete_missing_event() -> None:
    repository = EventRepository()

    assert repository.delete("missing") is False


def test_empty_event_id_is_rejected() -> None:
    repository = EventRepository()

    with pytest.raises(ValueError):
        repository.save(make_event(""))

    with pytest.raises(ValueError):
        repository.get("")

    with pytest.raises(ValueError):
        repository.exists("")

    with pytest.raises(ValueError):
        repository.delete("")