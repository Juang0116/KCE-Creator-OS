from datetime import datetime, timezone
from typing import Optional

from .models import (
    ExecutionLineage,
    ExecutionProcessing,
    ExecutionResult,
    ExecutionStage,
)

from src.production.engine import ProductionEngineV0
from src.qa.engine import QAEngineV0
from src.thumbnail.engine import ThumbnailEngineV0
from src.metadata.engine import MetadataEngineV0
from src.approval.engine import ApprovalEngineV0
from src.publish.engine import PublishEngineV0


class ExecutionEngineV0:
    """
    Deterministic orchestration layer for the KCE Creator OS pipeline.

    Execution coordinates existing engines.
    It does not render media, call external APIs, or publish content.
    """

    def __init__(
        self,
        production_engine=None,
        qa_engine=None,
        thumbnail_engine=None,
        metadata_engine=None,
        approval_engine=None,
        publish_engine=None,
    ):
        self.production_engine = (
            production_engine or ProductionEngineV0()
        )
        self.qa_engine = qa_engine or QAEngineV0()
        self.thumbnail_engine = (
            thumbnail_engine or ThumbnailEngineV0()
        )
        self.metadata_engine = (
            metadata_engine or MetadataEngineV0()
        )
        self.approval_engine = (
            approval_engine or ApprovalEngineV0()
        )
        self.publish_engine = (
            publish_engine or PublishEngineV0()
        )

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def _lineage_from_storyboard(storyboard) -> ExecutionLineage:
        source = storyboard.source

        return ExecutionLineage(
            storyboard_id=storyboard.storyboard_id,
            script_id=source.script_id,
            idea_id=source.idea_id,
            opportunity_id=source.opportunity_id,
            signal_id=source.signal_id,
        )

    @staticmethod
    def _stage(
        name: str,
        status: str,
        artifact_id: str = "",
        message: str = "",
    ) -> ExecutionStage:
        return ExecutionStage(
            name=name,
            status=status,
            artifact_id=artifact_id,
            message=message,
        )

    def run(
        self,
        storyboard,
        asset_plan,
        voice_plan,
        music_sfx_plan,
        approval_plan=None,
        required_assets_ready: bool = True,
    ) -> ExecutionResult:
        """
        Execute the preparation pipeline.

        If approval_plan is omitted, ApprovalEngineV0 creates a pending
        human-review gate.

        If an approved approval_plan is supplied, PublishEngineV0 may
        produce a ready publication plan.

        No external publication occurs.
        """

        created_at = self._now()
        execution_id = f"execution_{storyboard.storyboard_id}"

        lineage = self._lineage_from_storyboard(storyboard)
        stages = []

        # ---------------------------------------------------------
        # 1. PRODUCTION
        # ---------------------------------------------------------

        production_plan = self.production_engine.generate(
            storyboard=storyboard,
            asset_plan=asset_plan,
            voice_plan=voice_plan,
            music_sfx_plan=music_sfx_plan,
        )

        stages.append(
            self._stage(
                name="production",
                status="completed",
                artifact_id=production_plan.production_plan_id,
            )
        )

        # ---------------------------------------------------------
        # 2. QA
        # ---------------------------------------------------------

        qa_report = self.qa_engine.generate(
            production_plan=production_plan,
            asset_plan=asset_plan,
            voice_plan=voice_plan,
            music_sfx_plan=music_sfx_plan,
        )

        qa_status = qa_report.summary.overall_status

        if qa_status == "failed":
            stages.append(
                self._stage(
                    name="qa",
                    status="failed",
                    artifact_id=qa_report.qa_report_id,
                    message="QA failed. Execution stopped.",
                )
            )

            return ExecutionResult(
                schema_version="1.0",
                execution_id=execution_id,
                created_at=created_at,
                execution_version="1",
                status="qa_failed",
                lineage=lineage,
                stages=stages,
                processing=ExecutionProcessing(
                    status="rejected",
                    confidence=qa_report.processing.confidence,
                    processed_at=self._now(),
                ),
            )

        stages.append(
            self._stage(
                name="qa",
                status="completed",
                artifact_id=qa_report.qa_report_id,
                message=qa_status,
            )
        )

        # ---------------------------------------------------------
        # 3. THUMBNAIL
        # ---------------------------------------------------------

        thumbnail_plan = self.thumbnail_engine.generate(
            production_plan=production_plan
        )

        stages.append(
            self._stage(
                name="thumbnail",
                status="completed",
                artifact_id=thumbnail_plan.thumbnail.thumbnail_id,
            )
        )

        # ---------------------------------------------------------
        # 4. METADATA
        # ---------------------------------------------------------

        metadata_plan = self.metadata_engine.generate(
            thumbnail_plan=thumbnail_plan
        )

        stages.append(
            self._stage(
                name="metadata",
                status="completed",
                artifact_id=metadata_plan.metadata_plan_id,
            )
        )

        # ---------------------------------------------------------
        # 5. APPROVAL
        # ---------------------------------------------------------

        if approval_plan is None:
            approval_plan = self.approval_engine.generate(
                production_plan=production_plan,
                qa_report=qa_report,
                thumbnail_plan=thumbnail_plan,
                metadata_plan=metadata_plan,
                required_assets_ready=required_assets_ready,
            )

        approval_status = approval_plan.decision.status

        if approval_status == "pending":
            approval_stage_status = "waiting"
        elif approval_status == "approved":
            approval_stage_status = "completed"
        else:
            approval_stage_status = "blocked"

        stages.append(
            self._stage(
                name="approval",
                status=approval_stage_status,
                artifact_id=approval_plan.approval_id,
                message=approval_status,
            )
        )

        # ---------------------------------------------------------
        # 6. PUBLISH PREPARATION
        # ---------------------------------------------------------

        publish_plan = self.publish_engine.generate(
            approval_plan=approval_plan,
            production_plan=production_plan,
            thumbnail_plan=thumbnail_plan,
            metadata_plan=metadata_plan,
        )

        publication_status = publish_plan.publication.status

        if publication_status == "ready":
            publish_stage_status = "completed"
        else:
            publish_stage_status = "blocked"

        stages.append(
            self._stage(
                name="publish",
                status=publish_stage_status,
                artifact_id=publish_plan.publish_plan_id,
                message=publication_status,
            )
        )

        # ---------------------------------------------------------
        # FINAL EXECUTION STATE
        # ---------------------------------------------------------

        if publication_status == "ready":
            execution_status = "ready_to_publish"
            processing_status = "approved"
        elif approval_status == "pending":
            execution_status = "awaiting_approval"
            processing_status = "review"
        else:
            execution_status = "blocked"
            processing_status = "rejected"

        return ExecutionResult(
            schema_version="1.0",
            execution_id=execution_id,
            created_at=created_at,
            execution_version="1",
            status=execution_status,
            lineage=lineage,
            stages=stages,
            processing=ExecutionProcessing(
                status=processing_status,
                confidence=1.0,
                processed_at=self._now(),
            ),
        )