from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from src.discovery import DiscoveryResult
from src.discovery_approval import DiscoveryApproval


@dataclass
class DiscoveryPackage:
    discovery: DiscoveryResult
    approval: Optional[DiscoveryApproval] = None

    def to_dict(self) -> dict:
        return {
            "discovery": self.discovery.to_dict(),
            "approval": (
                self.approval.to_dict()
                if self.approval is not None
                else None
            ),
        }


@dataclass
class ContentPipelineLineage:
    discovery_id: str = ""
    signal_id: str = ""
    opportunity_id: str = ""
    idea_id: str = ""
    research_id: str = ""
    fact_check_id: str = ""
    script_id: str = ""
    voice_plan_id: str = ""
    storyboard_id: str = ""
    asset_plan_id: str = ""
    music_sfx_plan_id: str = ""
    execution_id: str = ""


@dataclass
class ContentPipelineStage:
    name: str
    status: str
    artifact_id: str = ""
    message: str = ""


@dataclass
class ContentPipelineArtifacts:
    research: Optional[Any] = None
    fact_check: Optional[Any] = None
    script: Optional[Any] = None
    voice_plan: Optional[Any] = None
    storyboard: Optional[Any] = None
    asset_plan: Optional[Any] = None
    music_sfx_plan: Optional[Any] = None
    execution: Optional[Any] = None


@dataclass
class ContentPipelineResult:
    pipeline_id: str
    created_at: str
    status: str
    lineage: ContentPipelineLineage
    stages: list[ContentPipelineStage] = field(
        default_factory=list
    )
    artifacts: ContentPipelineArtifacts = field(
        default_factory=ContentPipelineArtifacts
    )