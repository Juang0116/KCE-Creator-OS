from src.events import Event


def test_event_creation() -> None:
    event = Event.create(
        event_id="event_001",
        event_type="discovery.created",
        entity_type="discovery",
        entity_id="discovery_001",
        payload={
            "source": "test",
        },
    )

    assert event.event_id == "event_001"
    assert event.event_type == "discovery.created"
    assert event.entity_type == "discovery"
    assert event.entity_id == "discovery_001"
    assert event.payload == {
        "source": "test",
    }
    assert event.created_at


def test_event_to_dict() -> None:
    event = Event(
        event_id="event_001",
        created_at="2026-09-10T00:00:00+00:00",
        event_type="idea.generated",
        entity_type="content_idea",
        entity_id="idea_001",
        payload={
            "test": True,
        },
    )

    assert event.to_dict() == {
        "event_id": "event_001",
        "created_at": "2026-09-10T00:00:00+00:00",
        "event_type": "idea.generated",
        "entity_type": "content_idea",
        "entity_id": "idea_001",
        "payload": {
            "test": True,
        },
    }


def test_event_defaults_empty_payload() -> None:
    event = Event.create(
        event_id="event_002",
        event_type="approval.requested",
        entity_type="discovery_approval",
        entity_id="approval_001",
    )

    assert event.payload == {}