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
    discovery.signal.platform = "YouTube"
    discovery.signal.to_dict.return_value = {
        "schema_version": "1.0.0",
        "signal_id": "signal_001",
        "source": {
            "type": "reddit",
            "platform": "YouTube",
            "url": "https://example.com/signal",
        },
        "signal": {
            "title": "Test signal",
            "summary": "Test summary",
        },
    }

    discovery.opportunity.opportunity_id = (
        "opportunity_001"
    )
    discovery.opportunity.signal_id = "signal_001"
    discovery.opportunity.brand_id = "brand_001"
    discovery.opportunity.channel = "Futuro Tech"
    discovery.opportunity.platform = "YouTube"
    discovery.opportunity.scoring.total_score = 82.5
    discovery.opportunity.analysis.recommendation = (
        "strong_candidate"
    )
    discovery.opportunity.to_dict.return_value = {
        "schema_version": "1.0.0",
        "opportunity_id": "opportunity_001",
        "source": {
            "signal_id": "signal_001",
        },
        "target": {
            "brand_id": "brand_001",
            "channel": "Futuro Tech",
            "platform": "YouTube",
        },
        "scoring": {
            "total_score": 82.5,
        },
        "analysis": {
            "recommendation": "strong_candidate",
        },
    }

    discovery.idea = Mock()
    discovery.idea.idea_id = "idea_001"
    discovery.idea.brand_id = "brand_001"
    discovery.idea.channel = "Futuro Tech"
    discovery.idea.platform = "YouTube"
    discovery.idea.opportunity_id = (
        "opportunity_001"
    )
    discovery.idea.signal_id = "signal_001"
    discovery.idea.concept.working_title = (
        "Test content idea"
    )
    discovery.idea.to_dict.return_value = {
        "schema_version": "1.0.0",
        "idea_id": "idea_001",
        "source": {
            "opportunity_id": "opportunity_001",
            "signal_id": "signal_001",
        },
        "target": {
            "brand_id": "brand_001",
            "channel": "Futuro Tech",
            "platform": "YouTube",
        },
        "concept": {
            "working_title": "Test content idea",
        },
    }

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


def make_package_with_approval() -> DiscoveryPackage:
    package = make_package()

    approval = Mock()

    approval.approval_id = "approval_001"
    approval.created_at = "2026-09-09T00:00:00Z"

    approval.source.discovery_id = "discovery_001"
    approval.source.idea_id = "idea_001"
    approval.source.opportunity_id = (
        "opportunity_001"
    )
    approval.source.signal_id = "signal_001"

    approval.target.brand_id = "brand_001"
    approval.target.channel = "Futuro Tech"
    approval.target.platform = "YouTube"

    approval.decision.status = "pending"
    approval.decision.decided_by = None
    approval.decision.decided_at = None
    approval.decision.notes = ""

    approval.processing.status = "pending"
    approval.processing.confidence = 1.0
    approval.processing.processed_at = None

    approval.to_dict.return_value = {
        "schema_version": "1.0.0",
        "approval_id": "approval_001",
        "created_at": "2026-09-09T00:00:00Z",
        "approval_version": "1",
        "source": {
            "discovery_id": "discovery_001",
            "idea_id": "idea_001",
            "opportunity_id": "opportunity_001",
            "signal_id": "signal_001",
        },
        "target": {
            "brand_id": "brand_001",
            "channel": "Futuro Tech",
            "platform": "YouTube",
        },
        "decision": {
            "status": "pending",
            "decided_by": None,
            "decided_at": None,
            "notes": "",
        },
        "processing": {
            "status": "pending",
            "confidence": 1.0,
            "processed_at": None,
        },
    }

    package.approval = approval

    package.to_dict.return_value = {
        "discovery": package.discovery.to_dict(),
        "approval": approval.to_dict(),
    }

    return package


def make_client() -> Mock:
    client = Mock()

    schema = client.schema.return_value

    tables = {
        "signals": Mock(),
        "opportunities": Mock(),
        "content_ideas": Mock(),
        "discoveries": Mock(),
        "discovery_approvals": Mock(),
    }

    def table_side_effect(name: str) -> Mock:
        return tables[name]

    schema.table.side_effect = table_side_effect

    return client


def get_table(
    client: Mock,
    table_name: str,
) -> Mock:
    return (
        client
        .schema("creator_os")
        .table(table_name)
    )


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

    table = get_table(
        client,
        "discoveries",
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


def test_save_persists_signal() -> None:
    client = make_client()

    repository = SupabaseDiscoveryPackageRepository(
        client
    )

    package = make_package()

    repository.save(
        key="discovery_001",
        value=package,
    )

    table = get_table(
        client,
        "signals",
    )

    table.upsert.assert_called_once()

    row = table.upsert.call_args.args[0]

    assert row["signal_id"] == "signal_001"
    assert row["brand_id"] is None
    assert row["channel"] is None
    assert row["platform"] == "YouTube"
    assert row["source"] == "reddit"
    assert row["title"] == "Test signal"
    assert row["url"] == (
        "https://example.com/signal"
    )
    assert row["payload"] == (
        package.discovery.signal.to_dict()
    )


def test_save_persists_opportunity() -> None:
    client = make_client()

    repository = SupabaseDiscoveryPackageRepository(
        client
    )

    package = make_package()

    repository.save(
        key="discovery_001",
        value=package,
    )

    table = get_table(
        client,
        "opportunities",
    )

    table.upsert.assert_called_once()

    row = table.upsert.call_args.args[0]

    assert row["opportunity_id"] == (
        "opportunity_001"
    )
    assert row["signal_id"] == "signal_001"
    assert row["brand_id"] == "brand_001"
    assert row["channel"] == "Futuro Tech"
    assert row["platform"] == "YouTube"
    assert row["total_score"] == 82.5
    assert row["recommendation"] == (
        "strong_candidate"
    )
    assert row["payload"] == (
        package.discovery.opportunity.to_dict()
    )


def test_save_persists_content_idea() -> None:
    client = make_client()

    repository = SupabaseDiscoveryPackageRepository(
        client
    )

    package = make_package()

    repository.save(
        key="discovery_001",
        value=package,
    )

    table = get_table(
        client,
        "content_ideas",
    )

    table.upsert.assert_called_once()

    row = table.upsert.call_args.args[0]

    assert row["idea_id"] == "idea_001"
    assert row["opportunity_id"] == (
        "opportunity_001"
    )
    assert row["signal_id"] == "signal_001"
    assert row["brand_id"] == "brand_001"
    assert row["channel"] == "Futuro Tech"
    assert row["platform"] == "YouTube"
    assert row["concept"] == "Test content idea"
    assert row["payload"] == (
        package.discovery.idea.to_dict()
    )


def test_save_skips_content_idea_when_missing() -> None:
    client = make_client()

    repository = SupabaseDiscoveryPackageRepository(
        client
    )

    package = make_package()
    package.discovery.idea = None

    repository.save(
        key="discovery_001",
        value=package,
    )

    table = get_table(
        client,
        "content_ideas",
    )

    table.upsert.assert_not_called()


def test_save_persists_discovery_snapshot() -> None:
    client = make_client()

    repository = SupabaseDiscoveryPackageRepository(
        client
    )

    package = make_package()

    repository.save(
        key="discovery_001",
        value=package,
    )

    table = get_table(
        client,
        "discoveries",
    )

    row = table.upsert.call_args.args[0]

    assert row["payload"] == package.to_dict()


def test_save_persists_approval() -> None:
    client = make_client()

    repository = SupabaseDiscoveryPackageRepository(
        client
    )

    package = make_package_with_approval()

    repository.save(
        key="discovery_001",
        value=package,
    )

    table = get_table(
        client,
        "discovery_approvals",
    )

    table.upsert.assert_called_once()

    row = table.upsert.call_args.args[0]

    assert row["approval_id"] == "approval_001"
    assert row["discovery_id"] == (
        "discovery_001"
    )
    assert row["idea_id"] == "idea_001"
    assert row["status"] == "pending"
    assert row["decided_by"] is None
    assert row["decided_at"] is None
    assert row["notes"] == ""
    assert row["payload"] == (
        package.approval.to_dict()
    )


def test_save_skips_approval_when_missing() -> None:
    client = make_client()

    repository = SupabaseDiscoveryPackageRepository(
        client
    )

    package = make_package()

    assert package.approval is None

    repository.save(
        key="discovery_001",
        value=package,
    )

    table = get_table(
        client,
        "discovery_approvals",
    )

    table.upsert.assert_not_called()


def test_save_preserves_lineage_across_normalized_rows() -> None:
    client = make_client()

    repository = SupabaseDiscoveryPackageRepository(
        client
    )

    package = make_package()

    repository.save(
        key="discovery_001",
        value=package,
    )

    signal_row = get_table(
        client,
        "signals",
    ).upsert.call_args.args[0]

    opportunity_row = get_table(
        client,
        "opportunities",
    ).upsert.call_args.args[0]

    idea_row = get_table(
        client,
        "content_ideas",
    ).upsert.call_args.args[0]

    discovery_row = get_table(
        client,
        "discoveries",
    ).upsert.call_args.args[0]

    assert signal_row["signal_id"] == "signal_001"

    assert opportunity_row["opportunity_id"] == (
        "opportunity_001"
    )
    assert opportunity_row["signal_id"] == (
        "signal_001"
    )

    assert idea_row["idea_id"] == "idea_001"
    assert idea_row["opportunity_id"] == (
        "opportunity_001"
    )
    assert idea_row["signal_id"] == (
        "signal_001"
    )

    assert discovery_row["discovery_id"] == (
        "discovery_001"
    )
    assert discovery_row["signal_id"] == (
        "signal_001"
    )
    assert discovery_row["opportunity_id"] == (
        "opportunity_001"
    )
    assert discovery_row["idea_id"] == "idea_001"


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