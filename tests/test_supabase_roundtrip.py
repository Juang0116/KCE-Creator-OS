from __future__ import annotations

from datetime import datetime, timezone

from src.brand_brain import BrandEvaluation
from src.content.ideas import (
    ContentAudience,
    ContentConcept,
    ContentIdea,
    ContentProcessing,
    ContentProduction,
    CreativeDirection,
)
from src.discovery import (
    DiscoveryProcessing,
    DiscoveryResult,
)
from src.discovery_approval import (
    DiscoveryApproval,
    DiscoveryApprovalDecision,
    DiscoveryApprovalProcessing,
    DiscoveryApprovalSource,
    DiscoveryApprovalTarget,
)
from src.integrations.supabase.repository import (
    SupabaseDiscoveryPackageRepository,
)
from src.opportunity import (
    Opportunity,
    OpportunityAnalysis,
    OpportunityProcessing,
    OpportunityScoring,
)
from src.orchestration import DiscoveryPackage
from src.radar import RadarSignal


def make_package() -> DiscoveryPackage:
    timestamp = datetime.now(
        timezone.utc
    ).isoformat()

    signal = RadarSignal(
        signal_id="signal_roundtrip_001",
        detected_at=timestamp,
        radar_version="1",
        source_type="reddit",
        platform="Reddit",
        url="https://example.com/post",
        author="creator",
        published_at=timestamp,
        title="Test signal",
        summary="Signal used for persistence testing.",
        keywords=[
            "test",
            "creator",
        ],
        topics=[
            "technology",
        ],
        language="es",
        evidence={
            "source_count": 2,
            "confidence_reason": "test",
        },
        niches=[
            "technology",
        ],
        relevance_reason="Relevant test signal.",
        status="detected",
        confidence=0.91,
        processed_at=timestamp,
    )

    brand_evaluation = BrandEvaluation(
        brand_id="brand_test",
        signal_id=signal.signal_id,
        relevant=True,
        relevance_score=8.5,
        matched_pillars=[
            "AI",
        ],
        matched_topics=[
            "creator tools",
        ],
        reason="Strong test relevance.",
        rule_flags=[
            "none",
        ],
        confidence=0.88,
    )

    opportunity = Opportunity(
        opportunity_id="opportunity_roundtrip_001",
        created_at=timestamp,
        opportunity_version="1",
        signal_id=signal.signal_id,
        brand_id="brand_test",
        channel="Futuro Tech",
        scoring=OpportunityScoring(
            relevance=9.0,
            audience_fit=8.0,
            trend_strength=9.0,
            novelty=7.0,
            production_feasibility=8.0,
            evergreen_potential=7.0,
            total_score=80.0,
        ),
        analysis=OpportunityAnalysis(
            why_now="Relevant now.",
            why_this_brand="Fits the brand.",
            risks=[
                "Test risk",
            ],
            recommendation="strong_candidate",
        ),
        processing=OpportunityProcessing(
            status="processed",
            confidence=0.92,
            processed_at=timestamp,
        ),
    )

    idea = ContentIdea(
        idea_id="idea_roundtrip_001",
        created_at=timestamp,
        idea_version="1",
        opportunity_id=opportunity.opportunity_id,
        signal_id=signal.signal_id,
        brand_id="brand_test",
        channel="Futuro Tech",
        platform="YouTube",
        concept=ContentConcept(
            working_title="Test Creator OS Video",
            hook="This is a test hook.",
            core_promise="Explain the test.",
            angle="Technical demonstration.",
            format="long_form",
            estimated_duration_seconds=600,
            content_pillar="AI",
        ),
        audience=ContentAudience(
            target="Creators",
            audience_need="Better workflows.",
            expected_value="Clear understanding.",
        ),
        creative_direction=CreativeDirection(
            storytelling_approach="Educational",
            visual_direction="Clean technical visuals",
            voice_direction="Confident",
            key_elements=[
                "diagrams",
                "examples",
            ],
        ),
        production=ContentProduction(
            complexity="medium",
            estimated_production_hours=3.5,
            required_assets=[
                "screen recording",
            ],
            ai_assistance=[
                "research",
                "script",
            ],
        ),
        processing=ContentProcessing(
            status="draft",
            confidence=0.85,
            processed_at=timestamp,
        ),
    )

    discovery = DiscoveryResult(
        discovery_id="discovery_roundtrip_001",
        created_at=timestamp,
        discovery_version="1",
        signal=signal,
        brand_evaluation=brand_evaluation,
        opportunity=opportunity,
        idea=idea,
        processing=DiscoveryProcessing(
            status="draft",
            confidence=0.84,
            processed_at=timestamp,
        ),
    )

    approval = DiscoveryApproval(
        schema_version="1.0.0",
        approval_id="discovery_approval_roundtrip_001",
        created_at=timestamp,
        approval_version="1",
        source=DiscoveryApprovalSource(
            discovery_id=discovery.discovery_id,
            idea_id=idea.idea_id,
            opportunity_id=opportunity.opportunity_id,
            signal_id=signal.signal_id,
        ),
        target=DiscoveryApprovalTarget(
            brand_id="brand_test",
            channel="Futuro Tech",
            platform="YouTube",
        ),
        decision=DiscoveryApprovalDecision(
            status="pending",
            notes="Waiting for human approval.",
        ),
        processing=DiscoveryApprovalProcessing(
            status="pending",
            confidence=1.0,
        ),
    )

    return DiscoveryPackage(
        discovery=discovery,
        approval=approval,
    )


def test_package_roundtrip() -> None:
    package = make_package()

    payload = package.to_dict()

    restored = (
        SupabaseDiscoveryPackageRepository
        ._package_from_row(
            {
                "payload": payload,
            }
        )
    )

    assert restored.to_dict() == payload


def test_package_roundtrip_preserves_lineage() -> None:
    package = make_package()

    restored = (
        SupabaseDiscoveryPackageRepository
        ._package_from_row(
            {
                "payload": package.to_dict(),
            }
        )
    )

    assert (
        restored.discovery.discovery_id
        == "discovery_roundtrip_001"
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


def test_package_roundtrip_preserves_nested_data() -> None:
    package = make_package()

    restored = (
        SupabaseDiscoveryPackageRepository
        ._package_from_row(
            {
                "payload": package.to_dict(),
            }
        )
    )

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