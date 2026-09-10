from __future__ import annotations

from src.config import Settings
from src.integrations.supabase import create_supabase_client
from src.integrations.supabase.repository import (
    SupabaseDiscoveryPackageRepository,
)
from tests.test_supabase_roundtrip import make_package


DISCOVERY_ID = "discovery_roundtrip_001"


def make_live_repository() -> SupabaseDiscoveryPackageRepository:
    settings = Settings.from_env()
    settings.validate()

    client = create_supabase_client(settings)

    return SupabaseDiscoveryPackageRepository(client)


def test_live_supabase_roundtrip() -> None:
    repo = make_live_repository()
    package = make_package()

    # Clean up any previous test residue.
    repo.delete(DISCOVERY_ID)

    # Save the complete DiscoveryPackage to real Supabase.
    repo.save(DISCOVERY_ID, package)

    # Confirm the record exists.
    assert repo.exists(DISCOVERY_ID) is True

    # Retrieve the package from real Supabase.
    restored = repo.get(DISCOVERY_ID)

    assert restored is not None

    # Verify complete serialization/deserialization fidelity.
    assert restored.to_dict() == package.to_dict()

    # Verify important lineage explicitly.
    assert (
        restored.discovery.discovery_id
        == DISCOVERY_ID
    )

    assert (
        restored.discovery.signal.signal_id
        == "signal_roundtrip_001"
    )

    assert (
        restored.discovery.opportunity.opportunity_id
        == "opportunity_roundtrip_001"
    )

    assert (
        restored.discovery.idea.idea_id
        == "idea_roundtrip_001"
    )

    assert (
        restored.approval.approval_id
        == "discovery_approval_roundtrip_001"
    )

    # Verify nested data survived the real database round-trip.
    assert (
        restored.discovery.signal.evidence
        == {
            "source_count": 2,
            "confidence_reason": "test",
        }
    )

    assert (
        restored.discovery.opportunity.scoring.total_score
        == 80.0
    )

    assert (
        restored.discovery.idea.concept.working_title
        == "Test Creator OS Video"
    )

    assert (
        restored.discovery.idea.production
        .estimated_production_hours
        == 3.5
    )

    assert (
        restored.approval.decision.notes
        == "Waiting for human approval."
    )

    # Clean up the integration-test record.
    repo.delete(DISCOVERY_ID)

    # Confirm deletion from real Supabase.
    assert repo.exists(DISCOVERY_ID) is False
    assert repo.get(DISCOVERY_ID) is None