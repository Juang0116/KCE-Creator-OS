from datetime import datetime, timezone
from uuid import uuid4

from src.research import ResearchBrief
from .models import (
    FactCheck,
    FactCheckCheck,
    FactCheckProcessing,
    FactCheckSummary,
)


class FactCheckEngineV0:
    def generate(
        self,
        research: ResearchBrief,
    ) -> FactCheck:
        checks = self._build_checks(research)

        summary = self._build_summary(checks)

        processing = FactCheckProcessing(
            status="draft",
            confidence=self._calculate_confidence(research),
            processed_at=datetime.now(timezone.utc).isoformat(),
        )

        return FactCheck(
            fact_check_id=f"fact_{uuid4().hex[:12]}",
            created_at=datetime.now(timezone.utc).isoformat(),
            fact_check_version="0.1.0",
            research_id=research.research_id,
            idea_id=research.idea_id,
            opportunity_id=research.opportunity_id,
            signal_id=research.signal_id,
            brand_id=research.brand_id,
            channel=research.channel,
            platform=research.platform,
            checks=checks,
            summary=summary,
            processing=processing,
        )

    @staticmethod
    def _build_checks(
        research: ResearchBrief,
    ) -> list[FactCheckCheck]:
        checks = []

        for index, finding in enumerate(
            research.findings,
            start=1,
        ):
            checks.append(
                FactCheckCheck(
                    check_id=f"check_{index:03d}",
                    claim=finding.claim,
                    evidence=finding.evidence,
                    source_ids=[finding.source_id],
                    verification_status="unverified",
                    confidence=finding.confidence,
                    notes=(
                        "Pendiente de verificación mediante "
                        "fuentes y evidencia adicional."
                    ),
                )
            )

        return checks

    @staticmethod
    def _build_summary(
        checks: list[FactCheckCheck],
    ) -> FactCheckSummary:
        verified = sum(
            check.verification_status == "verified"
            for check in checks
        )

        partially_verified = sum(
            check.verification_status == "partially_verified"
            for check in checks
        )

        unverified = sum(
            check.verification_status == "unverified"
            for check in checks
        )

        refuted = sum(
            check.verification_status == "refuted"
            for check in checks
        )

        conflicting = sum(
            check.verification_status == "conflicting"
            for check in checks
        )

        return FactCheckSummary(
            total_claims=len(checks),
            verified_claims=verified,
            partially_verified_claims=partially_verified,
            unverified_claims=unverified,
            refuted_claims=refuted,
            conflicting_claims=conflicting,
        )

    @staticmethod
    def _calculate_confidence(
        research: ResearchBrief,
    ) -> float:
        if not research.findings:
            return 0.0

        total_confidence = sum(
            finding.confidence
            for finding in research.findings
        )

        return min(
            max(total_confidence / len(research.findings), 0.0),
            1.0,
        )