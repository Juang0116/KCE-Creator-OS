from datetime import datetime

import pytest

from src.discovery_approval import (
    DiscoveryApproval,
    DiscoveryApprovalDecisionEngineV0,
    DiscoveryApprovalEngineV0,
)


def make_approval() -> DiscoveryApproval:
    """
    Creates a minimal valid DiscoveryApproval fixture.
    """
    discovery = type(
        "Discovery",
        (),
        {
            "discovery_id": "discovery_001",
            "idea": type(
                "Idea",
                (),
                {
                    "idea_id": "idea_001",
                    "brand_id": "brand_001",
                    "channel": "Test Channel",
                    "platform": "youtube",
                },
            )(),
            "opportunity": type(
                "Opportunity",
                (),
                {
                    "opportunity_id": "opportunity_001",
                },
            )(),
            "signal": type(
                "Signal",
                (),
                {
                    "signal_id": "signal_001",
                },
            )(),
        },
    )()

    return DiscoveryApprovalEngineV0().generate(discovery)


def test_pending_approval_can_be_approved():
    approval = make_approval()
    engine = DiscoveryApprovalDecisionEngineV0()

    result = engine.decide(
        approval=approval,
        decision="approved",
        decided_by="juancho",
        notes="Approved for research.",
        decided_at="2026-09-11T21:00:00+00:00",
    )

    assert result is approval
    assert result.decision.status == "approved"
    assert result.decision.decided_by == "juancho"
    assert result.decision.decided_at == "2026-09-11T21:00:00+00:00"
    assert result.decision.notes == "Approved for research."

    assert result.processing.status == "completed"
    assert result.processing.confidence == 1.0
    assert result.processing.processed_at == "2026-09-11T21:00:00+00:00"


def test_pending_approval_can_be_rejected():
    approval = make_approval()
    engine = DiscoveryApprovalDecisionEngineV0()

    result = engine.decide(
        approval=approval,
        decision="rejected",
        decided_by="juancho",
        notes="Does not fit the current strategy.",
        decided_at="2026-09-11T21:05:00+00:00",
    )

    assert result.decision.status == "rejected"
    assert result.decision.decided_by == "juancho"
    assert result.decision.notes == "Does not fit the current strategy."
    assert result.processing.status == "completed"
    assert result.processing.confidence == 1.0


def test_approved_approval_cannot_be_decided_again():
    approval = make_approval()
    engine = DiscoveryApprovalDecisionEngineV0()

    engine.decide(
        approval=approval,
        decision="approved",
        decided_by="juancho",
    )

    with pytest.raises(ValueError, match="Only pending approvals can be decided"):
        engine.decide(
            approval=approval,
            decision="rejected",
            decided_by="juancho",
        )


def test_rejected_approval_cannot_be_decided_again():
    approval = make_approval()
    engine = DiscoveryApprovalDecisionEngineV0()

    engine.decide(
        approval=approval,
        decision="rejected",
        decided_by="juancho",
    )

    with pytest.raises(ValueError, match="Only pending approvals can be decided"):
        engine.decide(
            approval=approval,
            decision="approved",
            decided_by="juancho",
        )


def test_invalid_decision_is_rejected():
    approval = make_approval()
    engine = DiscoveryApprovalDecisionEngineV0()

    with pytest.raises(
        ValueError,
        match="Decision must be 'approved' or 'rejected'",
    ):
        engine.decide(
            approval=approval,
            decision="pending",
            decided_by="juancho",
        )


def test_empty_decided_by_is_rejected():
    approval = make_approval()
    engine = DiscoveryApprovalDecisionEngineV0()

    with pytest.raises(
        ValueError,
        match="decided_by must not be empty",
    ):
        engine.decide(
            approval=approval,
            decision="approved",
            decided_by="",
        )


def test_none_approval_is_rejected():
    engine = DiscoveryApprovalDecisionEngineV0()

    with pytest.raises(
        ValueError,
        match="Discovery approval cannot be None",
    ):
        engine.decide(
            approval=None,
            decision="approved",
            decided_by="juancho",
        )


def test_decided_at_is_generated_when_not_provided():
    approval = make_approval()
    engine = DiscoveryApprovalDecisionEngineV0()

    result = engine.decide(
        approval=approval,
        decision="approved",
        decided_by="juancho",
    )

    assert result.decision.decided_at is not None
    assert result.processing.processed_at is not None

    datetime.fromisoformat(result.decision.decided_at)
    datetime.fromisoformat(result.processing.processed_at)