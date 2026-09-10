from __future__ import annotations

from typing import Any

from supabase import Client

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
from src.opportunity import (
    Opportunity,
    OpportunityAnalysis,
    OpportunityProcessing,
    OpportunityScoring,
)
from src.orchestration import DiscoveryPackage
from src.persistence import Repository
from src.radar import RadarSignal


class SupabaseDiscoveryPackageRepository(
    Repository[DiscoveryPackage]
):
    """
    Supabase-backed repository for DiscoveryPackage objects.

    V1 persistence strategy:

    - Persist upstream domain entities in normalized tables:
        signals
        opportunities
        content_ideas

    - Persist the discovery aggregate in:
        discoveries

    - Persist the optional discovery approval in:
        discovery_approvals

    - Keep the complete DiscoveryPackage snapshot inside
      discoveries.payload for stable aggregate reconstruction.

    Reads intentionally continue to use the aggregate snapshot.
    Normalized tables are currently used for persistence and
    future querying, not for aggregate reconstruction.
    """

    TABLE_NAME = "discoveries"
    SIGNALS_TABLE = "signals"
    OPPORTUNITIES_TABLE = "opportunities"
    CONTENT_IDEAS_TABLE = "content_ideas"
    APPROVALS_TABLE = "discovery_approvals"

    def __init__(self, client: Client) -> None:
        self.client = client

    # ------------------------------------------------------------------
    # Table helpers
    # ------------------------------------------------------------------

    def _table(self, table_name: str) -> Any:
        return (
            self.client
            .schema("creator_os")
            .table(table_name)
        )

    # ------------------------------------------------------------------
    # Normalized serialization
    # ------------------------------------------------------------------

    @staticmethod
    def _row_from_signal(
        signal: RadarSignal,
    ) -> dict[str, Any]:
        data = signal.to_dict()

        source = data.get("source", {})
        signal_data = data.get("signal", {})

        return {
            "signal_id": signal.signal_id,
            "created_at": signal.detected_at,
            "brand_id": None,
            "channel": None,
            "platform": source.get("platform"),
            "source": source.get("type"),
            "title": signal_data.get("title"),
            "url": source.get("url"),
            "payload": data,
        }

    @staticmethod
    def _row_from_opportunity(
        opportunity: Opportunity,
    ) -> dict[str, Any]:
        data = opportunity.to_dict()

        source = data.get("source", {})
        target = data.get("target", {})
        scoring = data.get("scoring", {})
        analysis = data.get("analysis", {})

        return {
            "opportunity_id": opportunity.opportunity_id,
            "created_at": opportunity.created_at,
            "signal_id": source.get("signal_id"),
            "brand_id": target.get("brand_id"),
            "channel": target.get("channel"),
            "platform": target.get("platform"),
            "total_score": scoring.get("total_score"),
            "recommendation": analysis.get(
                "recommendation"
            ),
            "payload": data,
        }

    @staticmethod
    def _row_from_content_idea(
        idea: ContentIdea,
    ) -> dict[str, Any]:
        data = idea.to_dict()

        source = data.get("source", {})
        target = data.get("target", {})
        concept = data.get("concept", {})

        return {
            "idea_id": idea.idea_id,
            "created_at": idea.created_at,
            "opportunity_id": source.get(
                "opportunity_id"
            ),
            "signal_id": source.get("signal_id"),
            "brand_id": target.get("brand_id"),
            "channel": target.get("channel"),
            "platform": target.get("platform"),
            "concept": concept.get("working_title"),
            "payload": data,
        }

    @staticmethod
    def _row_from_approval(
        approval: DiscoveryApproval,
    ) -> dict[str, Any]:
        data = approval.to_dict()

        source = data.get("source", {})
        decision = data.get("decision", {})

        return {
            "approval_id": approval.approval_id,
            "created_at": approval.created_at,
            "discovery_id": source.get(
                "discovery_id"
            ),
            "idea_id": source.get("idea_id"),
            "status": decision.get(
                "status",
                "pending",
            ),
            "decided_by": decision.get(
                "decided_by"
            ),
            "decided_at": decision.get(
                "decided_at"
            ),
            "notes": decision.get(
                "notes",
                "",
            ),
            "payload": data,
        }

    @staticmethod
    def _row_from_discovery(
        package: DiscoveryPackage,
    ) -> dict[str, Any]:
        discovery = package.discovery
        signal = discovery.signal
        opportunity = discovery.opportunity
        idea = discovery.idea
        approval = package.approval

        return {
            "discovery_id": discovery.discovery_id,
            "created_at": discovery.created_at,
            "idea_id": (
                idea.idea_id
                if idea is not None
                else None
            ),
            "opportunity_id": (
                opportunity.opportunity_id
            ),
            "signal_id": signal.signal_id,
            "approval_id": (
                approval.approval_id
                if approval is not None
                else None
            ),
            "brand_id": (
                idea.brand_id
                if idea is not None
                else discovery.brand_evaluation.brand_id
            ),
            "channel": (
                idea.channel
                if idea is not None
                else ""
            ),
            "platform": (
                idea.platform
                if idea is not None
                else signal.platform
            ),
            "status": discovery.processing.status,
            "payload": package.to_dict(),
        }

    # ------------------------------------------------------------------
    # Deserialization helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _signal_from_dict(
        data: dict[str, Any],
    ) -> RadarSignal:
        source = data.get("source", {})
        signal = data.get("signal", {})
        relevance = data.get("relevance", {})
        processing = data.get("processing", {})

        return RadarSignal(
            signal_id=data["signal_id"],
            detected_at=data["detected_at"],
            radar_version=data["radar_version"],
            source_type=source.get("type", ""),
            platform=source.get("platform", ""),
            url=source.get("url"),
            author=source.get("author"),
            published_at=source.get("published_at"),
            title=signal.get("title", ""),
            summary=signal.get("summary", ""),
            keywords=signal.get("keywords", []),
            topics=signal.get("topics", []),
            language=signal.get("language", "es"),
            evidence=data.get("evidence", {}),
            niches=relevance.get("niches", []),
            relevance_reason=relevance.get(
                "relevance_reason",
                "",
            ),
            status=processing.get(
                "status",
                "detected",
            ),
            confidence=processing.get(
                "confidence",
                0.0,
            ),
            processed_at=processing.get(
                "processed_at"
            ),
        )

    @staticmethod
    def _brand_evaluation_from_dict(
        data: dict[str, Any],
    ) -> BrandEvaluation:
        return BrandEvaluation(
            brand_id=data["brand_id"],
            signal_id=data["signal_id"],
            relevant=data["relevant"],
            relevance_score=data["relevance_score"],
            matched_pillars=data.get(
                "matched_pillars",
                [],
            ),
            matched_topics=data.get(
                "matched_topics",
                [],
            ),
            reason=data.get(
                "reason",
                "",
            ),
            rule_flags=data.get(
                "rule_flags",
                [],
            ),
            confidence=data.get(
                "confidence",
                0.0,
            ),
        )

    @staticmethod
    def _opportunity_from_dict(
        data: dict[str, Any],
    ) -> Opportunity:
        source = data.get("source", {})
        target = data.get("target", {})
        scoring = data.get("scoring", {})
        analysis = data.get("analysis", {})
        processing = data.get("processing", {})

        return Opportunity(
            opportunity_id=data["opportunity_id"],
            created_at=data["created_at"],
            opportunity_version=data[
                "opportunity_version"
            ],
            signal_id=source.get(
                "signal_id",
                "",
            ),
            brand_id=target.get(
                "brand_id",
                "",
            ),
            channel=target.get(
                "channel",
                "",
            ),
            scoring=OpportunityScoring(
                relevance=scoring.get(
                    "relevance",
                    0.0,
                ),
                audience_fit=scoring.get(
                    "audience_fit",
                    0.0,
                ),
                trend_strength=scoring.get(
                    "trend_strength",
                    0.0,
                ),
                novelty=scoring.get(
                    "novelty",
                    0.0,
                ),
                production_feasibility=scoring.get(
                    "production_feasibility",
                    0.0,
                ),
                evergreen_potential=scoring.get(
                    "evergreen_potential",
                    0.0,
                ),
                total_score=scoring.get(
                    "total_score",
                    0.0,
                ),
            ),
            analysis=OpportunityAnalysis(
                why_now=analysis.get(
                    "why_now",
                    "",
                ),
                why_this_brand=analysis.get(
                    "why_this_brand",
                    "",
                ),
                risks=analysis.get(
                    "risks",
                    [],
                ),
                recommendation=analysis.get(
                    "recommendation",
                    "candidate",
                ),
            ),
            processing=OpportunityProcessing(
                status=processing.get(
                    "status",
                    "pending",
                ),
                confidence=processing.get(
                    "confidence",
                    0.0,
                ),
                processed_at=processing.get(
                    "processed_at"
                ),
            ),
        )

    @staticmethod
    def _content_idea_from_dict(
        data: dict[str, Any],
    ) -> ContentIdea:
        source = data.get("source", {})
        target = data.get("target", {})
        concept = data.get("concept", {})
        audience = data.get("audience", {})
        creative = data.get(
            "creative_direction",
            {},
        )
        production = data.get(
            "production",
            {},
        )
        processing = data.get(
            "processing",
            {},
        )

        return ContentIdea(
            idea_id=data["idea_id"],
            created_at=data["created_at"],
            idea_version=data["idea_version"],
            opportunity_id=source.get(
                "opportunity_id",
                "",
            ),
            signal_id=source.get(
                "signal_id",
                "",
            ),
            brand_id=target.get(
                "brand_id",
                "",
            ),
            channel=target.get(
                "channel",
                "",
            ),
            platform=target.get(
                "platform",
                "",
            ),
            concept=ContentConcept(
                working_title=concept.get(
                    "working_title",
                    "",
                ),
                hook=concept.get(
                    "hook",
                    "",
                ),
                core_promise=concept.get(
                    "core_promise",
                    "",
                ),
                angle=concept.get(
                    "angle",
                    "",
                ),
                format=concept.get(
                    "format",
                    "",
                ),
                estimated_duration_seconds=concept.get(
                    "estimated_duration_seconds",
                    0,
                ),
                content_pillar=concept.get(
                    "content_pillar",
                    "",
                ),
            ),
            audience=ContentAudience(
                target=audience.get(
                    "target",
                    "",
                ),
                audience_need=audience.get(
                    "audience_need",
                    "",
                ),
                expected_value=audience.get(
                    "expected_value",
                    "",
                ),
            ),
            creative_direction=CreativeDirection(
                storytelling_approach=creative.get(
                    "storytelling_approach",
                    "",
                ),
                visual_direction=creative.get(
                    "visual_direction",
                    "",
                ),
                voice_direction=creative.get(
                    "voice_direction",
                    "",
                ),
                key_elements=creative.get(
                    "key_elements",
                    [],
                ),
            ),
            production=ContentProduction(
                complexity=production.get(
                    "complexity",
                    "",
                ),
                estimated_production_hours=production.get(
                    "estimated_production_hours",
                    0.0,
                ),
                required_assets=production.get(
                    "required_assets",
                    [],
                ),
                ai_assistance=production.get(
                    "ai_assistance",
                    [],
                ),
            ),
            processing=ContentProcessing(
                status=processing.get(
                    "status",
                    "draft",
                ),
                confidence=processing.get(
                    "confidence",
                    0.0,
                ),
                processed_at=processing.get(
                    "processed_at"
                ),
            ),
        )

    @staticmethod
    def _discovery_from_dict(
        data: dict[str, Any],
    ) -> DiscoveryResult:
        signal = (
            SupabaseDiscoveryPackageRepository
            ._signal_from_dict(
                data["signal"]
            )
        )

        brand_evaluation = (
            SupabaseDiscoveryPackageRepository
            ._brand_evaluation_from_dict(
                data["brand_evaluation"]
            )
        )

        opportunity = (
            SupabaseDiscoveryPackageRepository
            ._opportunity_from_dict(
                data["opportunity"]
            )
        )

        idea_data = data.get("idea")

        idea = (
            SupabaseDiscoveryPackageRepository
            ._content_idea_from_dict(
                idea_data
            )
            if idea_data is not None
            else None
        )

        processing = data.get(
            "processing",
            {},
        )

        return DiscoveryResult(
            discovery_id=data["discovery_id"],
            created_at=data["created_at"],
            discovery_version=data[
                "discovery_version"
            ],
            signal=signal,
            brand_evaluation=brand_evaluation,
            opportunity=opportunity,
            idea=idea,
            processing=DiscoveryProcessing(
                status=processing.get(
                    "status",
                    "draft",
                ),
                confidence=processing.get(
                    "confidence",
                    0.0,
                ),
                processed_at=processing.get(
                    "processed_at"
                ),
            ),
        )

    @staticmethod
    def _approval_from_dict(
        data: dict[str, Any],
    ) -> DiscoveryApproval:
        source = data.get("source", {})
        target = data.get("target", {})
        decision = data.get(
            "decision",
            {},
        )
        processing = data.get(
            "processing",
            {},
        )

        return DiscoveryApproval(
            schema_version=data[
                "schema_version"
            ],
            approval_id=data["approval_id"],
            created_at=data["created_at"],
            approval_version=data[
                "approval_version"
            ],
            source=DiscoveryApprovalSource(
                discovery_id=source.get(
                    "discovery_id",
                    "",
                ),
                idea_id=source.get(
                    "idea_id",
                    "",
                ),
                opportunity_id=source.get(
                    "opportunity_id",
                    "",
                ),
                signal_id=source.get(
                    "signal_id",
                    "",
                ),
            ),
            target=DiscoveryApprovalTarget(
                brand_id=target.get(
                    "brand_id",
                    "",
                ),
                channel=target.get(
                    "channel",
                    "",
                ),
                platform=target.get(
                    "platform",
                    "",
                ),
            ),
            decision=DiscoveryApprovalDecision(
                status=decision.get(
                    "status",
                    "pending",
                ),
                decided_by=decision.get(
                    "decided_by"
                ),
                decided_at=decision.get(
                    "decided_at"
                ),
                notes=decision.get(
                    "notes",
                    "",
                ),
            ),
            processing=DiscoveryApprovalProcessing(
                status=processing.get(
                    "status",
                    "pending",
                ),
                confidence=processing.get(
                    "confidence",
                    0.0,
                ),
                processed_at=processing.get(
                    "processed_at"
                ),
            ),
        )

    @staticmethod
    def _package_from_row(
        row: dict[str, Any],
    ) -> DiscoveryPackage:
        payload = row["payload"]

        discovery = (
            SupabaseDiscoveryPackageRepository
            ._discovery_from_dict(
                payload["discovery"]
            )
        )

        approval_data = payload.get(
            "approval"
        )

        approval = (
            SupabaseDiscoveryPackageRepository
            ._approval_from_dict(
                approval_data
            )
            if approval_data is not None
            else None
        )

        return DiscoveryPackage(
            discovery=discovery,
            approval=approval,
        )

    # ------------------------------------------------------------------
    # Approval cleanup
    # ------------------------------------------------------------------

    def _delete_approvals_for_discovery(
        self,
        discovery_id: str,
    ) -> None:
        (
            self._table(self.APPROVALS_TABLE)
            .delete()
            .eq(
                "discovery_id",
                discovery_id,
            )
            .execute()
        )

    # ------------------------------------------------------------------
    # Repository contract
    # ------------------------------------------------------------------

    def save(
        self,
        key: str,
        value: DiscoveryPackage,
    ) -> DiscoveryPackage:
        if not key:
            raise ValueError(
                "Repository key must not be empty."
            )

        if (
            value.discovery.discovery_id
            != key
        ):
            raise ValueError(
                "Repository key must match "
                "DiscoveryPackage.discovery.discovery_id."
            )

        discovery = value.discovery
        signal = discovery.signal
        opportunity = discovery.opportunity
        idea = discovery.idea
        approval = value.approval

        # --------------------------------------------------------------
        # 1. Persist RadarSignal
        # --------------------------------------------------------------
        (
            self._table(self.SIGNALS_TABLE)
            .upsert(
                self._row_from_signal(signal),
                on_conflict="signal_id",
            )
            .execute()
        )

        # --------------------------------------------------------------
        # 2. Persist Opportunity
        # --------------------------------------------------------------
        (
            self._table(self.OPPORTUNITIES_TABLE)
            .upsert(
                self._row_from_opportunity(
                    opportunity
                ),
                on_conflict="opportunity_id",
            )
            .execute()
        )

        # --------------------------------------------------------------
        # 3. Persist ContentIdea when present
        # --------------------------------------------------------------
        if idea is not None:
            (
                self._table(self.CONTENT_IDEAS_TABLE)
                .upsert(
                    self._row_from_content_idea(
                        idea
                    ),
                    on_conflict="idea_id",
                )
                .execute()
            )

        # --------------------------------------------------------------
        # 4. Persist Discovery aggregate snapshot
        # --------------------------------------------------------------
        (
            self._table(self.TABLE_NAME)
            .upsert(
                self._row_from_discovery(value),
                on_conflict="discovery_id",
            )
            .execute()
        )

        # --------------------------------------------------------------
        # 5. Persist DiscoveryApproval when present
        #
        # Remove previous approvals for this discovery first.
        # Approval IDs are generated independently, so simply upserting
        # a new approval could otherwise leave an orphaned old approval.
        # --------------------------------------------------------------
        self._delete_approvals_for_discovery(
            discovery.discovery_id
        )

        if approval is not None:
            (
                self._table(self.APPROVALS_TABLE)
                .upsert(
                    self._row_from_approval(
                        approval
                    ),
                    on_conflict="approval_id",
                )
                .execute()
            )

        return value

    def get(
        self,
        key: str,
    ) -> DiscoveryPackage | None:
        if not key:
            raise ValueError(
                "Repository key must not be empty."
            )

        response = (
            self._table(self.TABLE_NAME)
            .select("payload")
            .eq(
                "discovery_id",
                key,
            )
            .limit(1)
            .execute()
        )

        if not response.data:
            return None

        return self._package_from_row(
            response.data[0]
        )

    def exists(
        self,
        key: str,
    ) -> bool:
        if not key:
            raise ValueError(
                "Repository key must not be empty."
            )

        response = (
            self._table(self.TABLE_NAME)
            .select("discovery_id")
            .eq(
                "discovery_id",
                key,
            )
            .limit(1)
            .execute()
        )

        return bool(response.data)

    def delete(
        self,
        key: str,
    ) -> bool:
        if not key:
            raise ValueError(
                "Repository key must not be empty."
            )

        # Approval belongs to the discovery aggregate,
        # while signal/opportunity/idea are upstream entities
        # that may be shared and therefore remain untouched.
        self._delete_approvals_for_discovery(
            key
        )

        response = (
            self._table(self.TABLE_NAME)
            .delete()
            .eq(
                "discovery_id",
                key,
            )
            .execute()
        )

        return bool(response.data)

    def list_all(
        self,
    ) -> list[DiscoveryPackage]:
        response = (
            self._table(self.TABLE_NAME)
            .select("payload")
            .execute()
        )

        return [
            self._package_from_row(row)
            for row in response.data
        ]