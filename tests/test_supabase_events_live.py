from __future__ import annotations

from uuid import uuid4

from src.config import Settings
from src.events import Event
from src.integrations.supabase import (
    SupabaseEventRepository,
    create_supabase_client,
)


def test_live_supabase_event_roundtrip():
    settings = Settings.from_env()
    client = create_supabase_client(settings)
    repository = SupabaseEventRepository(client)

    event_id = f"event_live_{uuid4().hex}"

    event = Event.create(
        event_id=event_id,
        event_type="test.event",
        entity_type="test",
        entity_id="live_test",
        payload={
            "source": "test_supabase_events_live",
            "value": 42,
        },
    )

    try:
        # SAVE
        saved = repository.save(event)

        assert saved.event_id == event_id

        # EXISTS
        assert repository.exists(event_id) is True

        # GET
        loaded = repository.get(event_id)

        assert loaded is not None
        assert loaded.event_id == event.event_id
        assert loaded.created_at == event.created_at
        assert loaded.event_type == event.event_type
        assert loaded.entity_type == event.entity_type
        assert loaded.entity_id == event.entity_id
        assert loaded.payload == event.payload

        # LIST
        events = repository.list_all()

        assert any(item.event_id == event_id for item in events)

    finally:
        # CLEANUP
        repository.delete(event_id)

    # VERIFY DELETE
    assert repository.exists(event_id) is False
    assert repository.get(event_id) is None