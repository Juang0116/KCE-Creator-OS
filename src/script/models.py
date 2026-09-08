from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ScriptSource:
    idea_id: str
    research_id: str
    fact_check_id: str
    opportunity_id: str
    signal_id: str

    def to_dict(self) -> dict:
        return {
            "idea_id": self.idea_id,
            "research_id": self.research_id,
            "fact_check_id": self.fact_check_id,
            "opportunity_id": self.opportunity_id,
            "signal_id": self.signal_id,
        }


@dataclass
class ScriptTarget:
    brand_id: str
    channel: str
    platform: str

    def to_dict(self) -> dict:
        return {
            "brand_id": self.brand_id,
            "channel": self.channel,
            "platform": self.platform,
        }


@dataclass
class ScriptMetadata:
    title: str
    format: str
    estimated_duration_seconds: int
    content_pillar: str
    tone: str

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "format": self.format,
            "estimated_duration_seconds": self.estimated_duration_seconds,
            "content_pillar": self.content_pillar,
            "tone": self.tone,
        }


@dataclass
class ScriptHook:
    narration: str
    visual_direction: str

    def to_dict(self) -> dict:
        return {
            "narration": self.narration,
            "visual_direction": self.visual_direction,
        }


@dataclass
class ScriptIntroduction:
    narration: str
    visual_direction: str

    def to_dict(self) -> dict:
        return {
            "narration": self.narration,
            "visual_direction": self.visual_direction,
        }


@dataclass
class ScriptClaim:
    claim: str
    fact_check_id: str
    verification_status: str

    def to_dict(self) -> dict:
        return {
            "claim": self.claim,
            "fact_check_id": self.fact_check_id,
            "verification_status": self.verification_status,
        }


@dataclass
class ScriptSection:
    section_id: str
    title: str
    narration: str
    claims: list[ScriptClaim] = field(default_factory=list)
    visual_direction: str = ""
    transition: str = ""

    def to_dict(self) -> dict:
        return {
            "section_id": self.section_id,
            "title": self.title,
            "narration": self.narration,
            "claims": [claim.to_dict() for claim in self.claims],
            "visual_direction": self.visual_direction,
            "transition": self.transition,
        }


@dataclass
class ScriptConclusion:
    narration: str
    visual_direction: str

    def to_dict(self) -> dict:
        return {
            "narration": self.narration,
            "visual_direction": self.visual_direction,
        }


@dataclass
class ScriptCTA:
    narration: str
    visual_direction: str

    def to_dict(self) -> dict:
        return {
            "narration": self.narration,
            "visual_direction": self.visual_direction,
        }


@dataclass
class ScriptProcessing:
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
class Script:
    schema_version: str
    script_id: str
    created_at: str
    script_version: str
    source: ScriptSource
    target: ScriptTarget
    metadata: ScriptMetadata
    hook: ScriptHook
    introduction: ScriptIntroduction
    sections: list[ScriptSection]
    conclusion: ScriptConclusion
    cta: ScriptCTA
    processing: ScriptProcessing

    def to_dict(self) -> dict:
        return {
            "schema_version": self.schema_version,
            "script_id": self.script_id,
            "created_at": self.created_at,
            "script_version": self.script_version,
            "source": self.source.to_dict(),
            "target": self.target.to_dict(),
            "metadata": self.metadata.to_dict(),
            "hook": self.hook.to_dict(),
            "introduction": self.introduction.to_dict(),
            "sections": [section.to_dict() for section in self.sections],
            "conclusion": self.conclusion.to_dict(),
            "cta": self.cta.to_dict(),
            "processing": self.processing.to_dict(),
        }