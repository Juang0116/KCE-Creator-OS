from dataclasses import dataclass

import pytest

from src.persistence import (
    MemoryRepository,
    Repository,
)


@dataclass
class ExampleRecord:
    record_id: str
    value: str


def test_memory_repository_starts_empty():
    repository = MemoryRepository[ExampleRecord]()

    assert repository.count() == 0
    assert repository.list_all() == []


def test_memory_repository_saves_record():
    repository = MemoryRepository[ExampleRecord]()

    record = ExampleRecord(
        record_id="record_001",
        value="hello",
    )

    result = repository.save(
        key=record.record_id,
        value=record,
    )

    assert result == record
    assert repository.count() == 1


def test_memory_repository_gets_record():
    repository = MemoryRepository[ExampleRecord]()

    record = ExampleRecord(
        record_id="record_001",
        value="hello",
    )

    repository.save(
        key=record.record_id,
        value=record,
    )

    result = repository.get(
        "record_001"
    )

    assert result == record


def test_memory_repository_returns_none_for_missing_record():
    repository = MemoryRepository[ExampleRecord]()

    assert (
        repository.get("missing")
        is None
    )


def test_memory_repository_checks_existence():
    repository = MemoryRepository[ExampleRecord]()

    record = ExampleRecord(
        record_id="record_001",
        value="hello",
    )

    assert (
        repository.exists("record_001")
        is False
    )

    repository.save(
        key=record.record_id,
        value=record,
    )

    assert (
        repository.exists("record_001")
        is True
    )


def test_memory_repository_replaces_existing_record():
    repository = MemoryRepository[ExampleRecord]()

    first = ExampleRecord(
        record_id="record_001",
        value="first",
    )

    second = ExampleRecord(
        record_id="record_001",
        value="second",
    )

    repository.save(
        key="record_001",
        value=first,
    )

    repository.save(
        key="record_001",
        value=second,
    )

    assert repository.count() == 1
    assert (
        repository.get("record_001")
        == second
    )


def test_memory_repository_lists_all_records():
    repository = MemoryRepository[ExampleRecord]()

    record_001 = ExampleRecord(
        record_id="record_001",
        value="first",
    )

    record_002 = ExampleRecord(
        record_id="record_002",
        value="second",
    )

    repository.save(
        key="record_001",
        value=record_001,
    )

    repository.save(
        key="record_002",
        value=record_002,
    )

    records = repository.list_all()

    assert len(records) == 2
    assert record_001 in records
    assert record_002 in records


def test_memory_repository_deletes_existing_record():
    repository = MemoryRepository[ExampleRecord]()

    record = ExampleRecord(
        record_id="record_001",
        value="hello",
    )

    repository.save(
        key=record.record_id,
        value=record,
    )

    result = repository.delete(
        "record_001"
    )

    assert result is True
    assert repository.count() == 0
    assert (
        repository.get("record_001")
        is None
    )


def test_memory_repository_delete_missing_record_returns_false():
    repository = MemoryRepository[ExampleRecord]()

    assert (
        repository.delete("missing")
        is False
    )


def test_memory_repository_rejects_empty_key():
    repository = MemoryRepository[ExampleRecord]()

    record = ExampleRecord(
        record_id="record_001",
        value="hello",
    )

    with pytest.raises(ValueError):
        repository.save(
            key="",
            value=record,
        )


def test_memory_repository_can_be_cleared():
    repository = MemoryRepository[ExampleRecord]()

    repository.save(
        key="record_001",
        value=ExampleRecord(
            record_id="record_001",
            value="first",
        ),
    )

    repository.save(
        key="record_002",
        value=ExampleRecord(
            record_id="record_002",
            value="second",
        ),
    )

    repository.clear()

    assert repository.count() == 0
    assert repository.list_all() == []


def test_memory_repository_matches_repository_protocol():
    repository = MemoryRepository[ExampleRecord]()

    protocol_repository: Repository[
        ExampleRecord
    ] = repository

    record = ExampleRecord(
        record_id="record_001",
        value="hello",
    )

    protocol_repository.save(
        key=record.record_id,
        value=record,
    )

    assert (
        protocol_repository.get(
            "record_001"
        )
        == record
    )