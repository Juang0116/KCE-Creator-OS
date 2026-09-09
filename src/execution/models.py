from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ExecutionLineage:
    storyboard_id: str
    script_id: str
    idea_id: str
    opportunity_id: str
    signal_id: str


@dataclass
class ExecutionStage:
    name: str
    status: str
    artifact_id: str = ""
    message: str = ""


@dataclass
class ExecutionProcessing:
    status: str = "draft"
    confidence: float = 0.0
    processed_at: Optional[str] = None


@dataclass
class ExecutionResult:
    schema_version: str
    execution_id: str
    created_at: str
    execution_version: str
    status: str
    lineage: ExecutionLineage
    stages: List[ExecutionStage] = field(default_factory=list)
    processing: ExecutionProcessing = field(
        default_factory=ExecutionProcessing
    )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)