from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from src.asset import AssetEngineV0
from src.discovery_approval import DiscoveryApproval
from src.execution import ExecutionEngineV0
from src.fact_check import FactCheckEngineV0
from src.music_sfx import MusicSFXEngineV0
from src.research import ResearchEngineV0
from src.script import ScriptEngineV0
from src.storyboard import StoryboardEngineV0
from src.voice import VoiceEngineV0

from .models import (
    ContentPipelineArtifacts,
    ContentPipelineLineage,
    ContentPipelineResult,
    ContentPipelineStage,
    DiscoveryPackage,
)


class ContentPipelineV0:
    """
    Orchestrates the content-production pipeline starting
    from an approved DiscoveryPackage.

    V0 is deterministic orchestration only.
    It does not generate media, publish content, or make
    autonomous strategic decisions.
    """

    def __init__(
        self,
        research_engine=None,
        fact_check_engine=None,
        script_engine=None,
        voice_engine=None,
        storyboard_engine=None,
        asset_engine=None,
        music_sfx_engine=None,
        execution_engine=None,
    ):
        self.research_engine = (
            research_engine or ResearchEngineV0()
        )
        self.fact_check_engine = (
            fact_check_engine or FactCheckEngineV0()
        )
        self.script_engine = (
            script_engine or ScriptEngineV0()
        )
        self.voice_engine = (
            voice_engine or VoiceEngineV0()
        )
        self.storyboard_engine = (
            storyboard_engine or StoryboardEngineV0()
        )
        self.asset_engine = (
            asset_engine or AssetEngineV0()
        )
        self.music_sfx_engine = (
            music_sfx_engine or MusicSFXEngineV0()
        )
        self.execution_engine = (
            execution_engine or ExecutionEngineV0()
        )

    @staticmethod
    def _approved(
        approval: Optional[DiscoveryApproval],
    ) -> bool:
        if approval is None:
            return False

        return approval.decision.status == "approved"

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def _stage(
        name: str,
        status: str,
        artifact_id: str = "",
        message: str = "",
    ) -> ContentPipelineStage:
        return ContentPipelineStage(
            name=name,
            status=status,
            artifact_id=artifact_id,
            message=message,
        )

    def run(
        self,
        discovery_package: DiscoveryPackage,
        brand,
        voice_profile,
    ) -> ContentPipelineResult:
        pipeline_id = (
            f"content_pipeline_{uuid4().hex[:12]}"
        )

        discovery = discovery_package.discovery
        approval = discovery_package.approval
        idea = discovery.idea

        lineage = ContentPipelineLineage(
            discovery_id=discovery.discovery_id,
            signal_id=(
                discovery.opportunity.signal_id
                if discovery.opportunity is not None
                else ""
            ),
            opportunity_id=(
                discovery.opportunity.opportunity_id
                if discovery.opportunity is not None
                else ""
            ),
            idea_id=(
                idea.idea_id
                if idea is not None
                else ""
            ),
        )

        stages: list[ContentPipelineStage] = []

        approval_id = (
            approval.approval_id
            if approval is not None
            else ""
        )

        # --------------------------------------------------
        # Discovery approval gate
        # --------------------------------------------------

        if not self._approved(approval):
            stages.append(
                self._stage(
                    name="discovery_approval",
                    status="blocked",
                    artifact_id=approval_id,
                    message=(
                        "Discovery approval is required "
                        "before content production can begin."
                    ),
                )
            )

            return ContentPipelineResult(
                pipeline_id=pipeline_id,
                created_at=self._now(),
                status="blocked",
                lineage=lineage,
                stages=stages,
                artifacts=ContentPipelineArtifacts(),
            )

        if idea is None:
            stages.append(
                self._stage(
                    name="discovery_approval",
                    status="blocked",
                    artifact_id=approval_id,
                    message=(
                        "An approved discovery must contain "
                        "a content idea."
                    ),
                )
            )

            return ContentPipelineResult(
                pipeline_id=pipeline_id,
                created_at=self._now(),
                status="blocked",
                lineage=lineage,
                stages=stages,
                artifacts=ContentPipelineArtifacts(),
            )

        stages.append(
            self._stage(
                name="discovery_approval",
                status="completed",
                artifact_id=approval_id,
                message="Discovery approved.",
            )
        )

        artifacts = ContentPipelineArtifacts()

        # --------------------------------------------------
        # Research
        # --------------------------------------------------

        research = self.research_engine.generate(
            idea=idea,
            brand=brand,
        )

        artifacts.research = research
        lineage.research_id = research.research_id

        stages.append(
            self._stage(
                name="research",
                status="completed",
                artifact_id=research.research_id,
            )
        )

        # --------------------------------------------------
        # Fact Check
        # --------------------------------------------------

        fact_check = self.fact_check_engine.generate(
            research=research,
        )

        artifacts.fact_check = fact_check
        lineage.fact_check_id = (
            fact_check.fact_check_id
        )

        stages.append(
            self._stage(
                name="fact_check",
                status="completed",
                artifact_id=fact_check.fact_check_id,
            )
        )

        # --------------------------------------------------
        # Script
        # --------------------------------------------------

        script = self.script_engine.generate(
            idea=idea,
            research=research,
            fact_check=fact_check,
        )

        artifacts.script = script
        lineage.script_id = script.script_id

        stages.append(
            self._stage(
                name="script",
                status="completed",
                artifact_id=script.script_id,
            )
        )

        # --------------------------------------------------
        # Voice
        # --------------------------------------------------

        voice_plan = self.voice_engine.generate(
            script=script,
            voice_profile=voice_profile,
        )

        artifacts.voice_plan = voice_plan
        lineage.voice_plan_id = (
            voice_plan.voice_plan_id
        )

        stages.append(
            self._stage(
                name="voice",
                status="completed",
                artifact_id=voice_plan.voice_plan_id,
            )
        )

        # --------------------------------------------------
        # Storyboard
        # --------------------------------------------------

        storyboard = self.storyboard_engine.generate(
            script=script,
        )

        artifacts.storyboard = storyboard
        lineage.storyboard_id = (
            storyboard.storyboard_id
        )

        stages.append(
            self._stage(
                name="storyboard",
                status="completed",
                artifact_id=storyboard.storyboard_id,
            )
        )

        # --------------------------------------------------
        # Assets
        # --------------------------------------------------

        asset_plan = self.asset_engine.generate(
            storyboard=storyboard,
        )

        artifacts.asset_plan = asset_plan
        lineage.asset_plan_id = (
            asset_plan.asset_plan_id
        )

        stages.append(
            self._stage(
                name="assets",
                status="completed",
                artifact_id=asset_plan.asset_plan_id,
            )
        )

        # --------------------------------------------------
        # Music / SFX
        # --------------------------------------------------

        music_sfx_plan = (
            self.music_sfx_engine.generate(
                storyboard=storyboard,
            )
        )

        artifacts.music_sfx_plan = music_sfx_plan
        lineage.music_sfx_plan_id = (
            music_sfx_plan.music_sfx_plan_id
        )

        stages.append(
            self._stage(
                name="music_sfx",
                status="completed",
                artifact_id=(
                    music_sfx_plan.music_sfx_plan_id
                ),
            )
        )

        # --------------------------------------------------
        # Execution
        # --------------------------------------------------

        execution = self.execution_engine.run(
            storyboard=storyboard,
            asset_plan=asset_plan,
            voice_plan=voice_plan,
            music_sfx_plan=music_sfx_plan,
        )

        artifacts.execution = execution
        lineage.execution_id = execution.execution_id

        if execution.status == "awaiting_approval":
            execution_stage_status = "waiting"
            pipeline_status = "awaiting_approval"
            execution_message = "awaiting_approval"

        elif execution.status == "ready_to_publish":
            execution_stage_status = "completed"
            pipeline_status = "completed"
            execution_message = "ready_to_publish"

        elif execution.status == "blocked":
            execution_stage_status = "blocked"
            pipeline_status = "blocked"
            execution_message = "blocked"

        else:
            execution_stage_status = "failed"
            pipeline_status = "failed"
            execution_message = execution.status

        stages.append(
            self._stage(
                name="execution",
                status=execution_stage_status,
                artifact_id=execution.execution_id,
                message=execution_message,
            )
        )

        return ContentPipelineResult(
            pipeline_id=pipeline_id,
            created_at=self._now(),
            status=pipeline_status,
            lineage=lineage,
            stages=stages,
            artifacts=artifacts,
        )