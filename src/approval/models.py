from dataclasses import dataclass


@dataclass
class ApprovalSource:
    production_plan_id: str
    qa_report_id: str
    thumbnail_plan_id: str
    metadata_plan_id: str
    storyboard_id: str
    script_id: str
    idea_id: str
    opportunity_id: str
    signal_id: str

    def to_dict(self):
        return {
            "production_plan_id": self.production_plan_id,
            "qa_report_id": self.qa_report_id,
            "thumbnail_plan_id": self.thumbnail_plan_id,
            "metadata_plan_id": self.metadata_plan_id,
            "storyboard_id": self.storyboard_id,
            "script_id": self.script_id,
            "idea_id": self.idea_id,
            "opportunity_id": self.opportunity_id,
            "signal_id": self.signal_id,
        }


@dataclass
class ApprovalTarget:
    brand_id: str
    channel: str
    platform: str

    def to_dict(self):
        return {
            "brand_id": self.brand_id,
            "channel": self.channel,
            "platform": self.platform,
        }


@dataclass
class ApprovalChecks:
    qa_passed: bool
    thumbnail_ready: bool
    metadata_ready: bool
    required_assets_ready: bool
    approval_required: bool

    def to_dict(self):
        return {
            "qa_passed": self.qa_passed,
            "thumbnail_ready": self.thumbnail_ready,
            "metadata_ready": self.metadata_ready,
            "required_assets_ready": self.required_assets_ready,
            "approval_required": self.approval_required,
        }


@dataclass
class ApprovalDecision:
    status: str = "pending"
    reason: str = ""
    approved_by: str = ""
    approved_at: str = ""

    def to_dict(self):
        return {
            "status": self.status,
            "reason": self.reason,
            "approved_by": self.approved_by,
            "approved_at": self.approved_at,
        }


@dataclass
class ApprovalProcessing:
    status: str = "draft"
    confidence: float = 0.0
    processed_at: str = ""

    def to_dict(self):
        return {
            "status": self.status,
            "confidence": self.confidence,
            "processed_at": self.processed_at,
        }


@dataclass
class ApprovalPlan:
    schema_version: str
    approval_id: str
    created_at: str
    approval_version: str
    source: ApprovalSource
    target: ApprovalTarget
    checks: ApprovalChecks
    decision: ApprovalDecision
    processing: ApprovalProcessing

    def to_dict(self):
        return {
            "schema_version": self.schema_version,
            "approval_id": self.approval_id,
            "created_at": self.created_at,
            "approval_version": self.approval_version,
            "source": self.source.to_dict(),
            "target": self.target.to_dict(),
            "checks": self.checks.to_dict(),
            "decision": self.decision.to_dict(),
            "processing": self.processing.to_dict(),
        }