from dataclasses import dataclass, field
from typing import Optional


@dataclass
class QAReportSource:
    production_plan_id: str
    storyboard_id: str
    asset_plan_id: str
    voice_plan_id: str
    music_sfx_plan_id: str
    script_id: str
    idea_id: str
    opportunity_id: str
    signal_id: str

    def to_dict(self) -> dict:
        return {
            "production_plan_id": self.production_plan_id,
            "storyboard_id": self.storyboard_id,
            "asset_plan_id": self.asset_plan_id,
            "voice_plan_id": self.voice_plan_id,
            "music_sfx_plan_id": self.music_sfx_plan_id,
            "script_id": self.script_id,
            "idea_id": self.idea_id,
            "opportunity_id": self.opportunity_id,
            "signal_id": self.signal_id,
        }


@dataclass
class QACheck:
    check_id: str
    category: str
    name: str
    status: str
    severity: str
    message: str

    def to_dict(self) -> dict:
        return {
            "check_id": self.check_id,
            "category": self.category,
            "name": self.name,
            "status": self.status,
            "severity": self.severity,
            "message": self.message,
        }


@dataclass
class QASummary:
    overall_status: str
    total_checks: int
    passed: int
    warnings: int
    failed: int

    def to_dict(self) -> dict:
        return {
            "overall_status": self.overall_status,
            "total_checks": self.total_checks,
            "passed": self.passed,
            "warnings": self.warnings,
            "failed": self.failed,
        }


@dataclass
class QAProcessing:
    status: str
    confidence: float
    processed_at: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "confidence": self.confidence,
            "processed_at": self.processed_at,
        }


@dataclass
class QAReport:
    schema_version: str
    qa_report_id: str
    created_at: str
    qa_version: str
    source: QAReportSource
    checks: list[QACheck] = field(default_factory=list)
    summary: QASummary = None
    processing: QAProcessing = None

    def to_dict(self) -> dict:
        return {
            "schema_version": self.schema_version,
            "qa_report_id": self.qa_report_id,
            "created_at": self.created_at,
            "qa_version": self.qa_version,
            "source": self.source.to_dict(),
            "checks": [check.to_dict() for check in self.checks],
            "summary": self.summary.to_dict(),
            "processing": self.processing.to_dict(),
        }