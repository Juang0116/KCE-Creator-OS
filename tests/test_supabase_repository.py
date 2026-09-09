from __future__ import annotations

from unittest.mock import Mock

import pytest

from src.integrations.supabase.repository import (
    SupabaseDiscoveryPackageRepository,
)
from src.orchestration import DiscoveryPackage


def make_package() -> DiscoveryPackage:
    discovery = Mock()

    discovery.discovery_id = "discovery_001"
    discovery.created_at = "2026-09-09T00:00:00Z"

    discovery.signal.signal_id = "signal_001"

    discovery.opportunity.opportunity_id = (
        "opportunity_001"
    )

    discovery.idea = Mock()
    discovery.idea.idea_id = "idea_001"
    discovery.idea.brand_id = "brand_001"
    discovery.idea.channel = "Futuro Tech"
    discovery.idea.platform = "YouTube"

    discovery.processing.status = "draft"

    discovery.to_dict.return_value = {
        "schema_version": "1.0.0",
        "discovery_id": "discovery_001",
    }

    package = Mock(spec=DiscoveryPackage)
    package.discovery = discovery
    package.approval = None
    package.to_dict.return_value = {
        "discovery": discovery.to_dict(),
        "approval": None,
    }

    return package


def make_client() -> Mock:
    client = Mock()

    schema = client.schema.return_value
    table = schema.table.return_value

    return client


def test_save_maps_package_to_supabase_row() -> None:
    client = make_client()

    repository = SupabaseDiscoveryPackageRepository(
        client
    )

    package = make_package()

    result = repository.save(
        key="discovery_001",
        value=package,
    )

    assert result is package

    table = (
        client
        .schema("creator_os")
        .table("discoveries")
    )

    table.upsert.assert_called_once()

    row = table.upsert.call_args.args[0]

    assert row["discovery_id"] == "discovery_001"
    assert row["signal_id"] == "signal_001"
    assert row["opportunity_id"] == (
        "opportunity_001"
    )
    assert row["idea_id"] == "idea_001"
    assert row["brand_id"] == "brand_001"
    assert row["channel"] == "Futuro Tech"
    assert row["platform"] == "YouTube"
    assert row["status"] == "draft"
    assert "payload" in row


def test_save_requires_matching_key() -> None:
    client = make_client()

    repository = SupabaseDiscoveryPackageRepository(
        client
    )

    package = make_package()

    with pytest.raises(ValueError):
        repository.save(
            key="different_id",
            value=package,
        )


def test_save_requires_non_empty_key() -> None:
    client = make_client()

    repository = SupabaseDiscoveryPackageRepository(
        client
    )

    package = make_package()

    with pytest.raises(ValueError):
        repository.save(
            key="",
            value=package,
        )


def test_get_missing_key_is_rejected() -> None:
    client = make_client()

    repository = SupabaseDiscoveryPackageRepository(
        client
    )

    with pytest.raises(ValueError):
        repository.get("")


def test_exists_missing_key_is_rejected() -> None:
    client = make_client()

    repository = SupabaseDiscoveryPackageRepository(
        client
    )

    with pytest.raises(ValueError):
        repository.exists("")


def test_delete_missing_key_is_rejected() -> None:
    client = make_client()

    repository = SupabaseDiscoveryPackageRepository(
        client
    )

    with pytest.raises(ValueError):
        repository.delete("")