from datetime import datetime, timezone

from .models import (
    ApprovalChecks,
    ApprovalDecision,
    ApprovalPlan,
    ApprovalProcessing,
    ApprovalSource,
    ApprovalTarget,
)


class ApprovalEngineV0:
    """
    Deterministic V0 approval gate.

    Evaluates whether the prepared content is structurally ready
    for human review. It never publishes content automatically.
    """

    def generate(
        self,
        production_plan,
        qa_report,
        thumbnail_plan,
        metadata_plan,
        required_assets_ready=True,
    ):
        processed_at = datetime.now(timezone.utc).isoformat()

        source = ApprovalSource(
            production_plan_id=production_plan.production_plan_id,
            qa_report_id=qa_report.qa_report_id,
            thumbnail_plan_id=thumbnail_plan.thumbnail_plan_id,
            metadata_plan_id=metadata_plan.metadata_plan_id,
            storyboard_id=thumbnail_plan.source.storyboard_id,
            script_id=thumbnail_plan.source.script_id,
            idea_id=thumbnail_plan.source.idea_id,
            opportunity_id=thumbnail_plan.source.opportunity_id,
            signal_id=thumbnail_plan.source.signal_id,
        )

        target = ApprovalTarget(
            brand_id=thumbnail_plan.target.brand_id,
            channel=thumbnail_plan.target.channel,
            platform=thumbnail_plan.target.platform,
        )

        qa_passed = qa_report.summary.overall_status == "passed"

        thumbnail_ready = (
            thumbnail_plan.thumbnail.status in {"planned", "generated", "approved"}
        )

        metadata_ready = (
            metadata_plan.metadata.status in {"planned", "draft", "review", "approved"}
        )

        checks = ApprovalChecks(
            qa_passed=qa_passed,
            thumbnail_ready=thumbnail_ready,
            metadata_ready=metadata_ready,
            required_assets_ready=required_assets_ready,
            approval_required=True,
        )

        all_checks_passed = (
            qa_passed
            and thumbnail_ready
            and metadata_ready
            and required_assets_ready
        )

        if all_checks_passed:
            reason = "Content package is ready for human approval."
        else:
            reason = "Content package requires changes before approval."

        decision = ApprovalDecision(
            status="pending",
            reason=reason,
            approved_by="",
            approved_at="",
        )

        processing = ApprovalProcessing(
            status="review",
            confidence=1.0 if all_checks_passed else 0.5,
            processed_at=processed_at,
        )

        return ApprovalPlan(
            schema_version="1.0",
            approval_id="approval_001",
            created_at=processed_at,
            approval_version="1",
            source=source,
            target=target,
            checks=checks,
            decision=decision,
            processing=processing,
        )