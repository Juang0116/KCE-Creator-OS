from datetime import datetime, timezone

from .models import (
    QAReport,
    QAReportSource,
    QACheck,
    QASummary,
    QAProcessing,
)


class QAEngineV0:
    """
    Deterministic QA Engine V0.

    Validates the structural integrity of a Production Plan
    and its related Asset, Voice and Music/SFX plans.

    V0 performs deterministic structural checks.
    It does not perform semantic AI review, media inspection,
    audio analysis or video rendering analysis yet.
    """

    def generate(
        self,
        production_plan,
        asset_plan,
        voice_plan,
        music_sfx_plan,
    ) -> QAReport:

        created_at = datetime.now(timezone.utc).isoformat()

        checks = []

        checks.append(
            self._check_production_timeline(production_plan)
        )

        checks.append(
            self._check_asset_references(
                production_plan,
                asset_plan,
            )
        )

        checks.append(
            self._check_voice_references(
                production_plan,
                voice_plan,
            )
        )

        checks.append(
            self._check_music_sfx_references(
                production_plan,
                music_sfx_plan,
            )
        )

        checks.append(
            self._check_timeline_continuity(production_plan)
        )

        checks.append(
            self._check_source_references(
                production_plan,
                asset_plan,
                voice_plan,
                music_sfx_plan,
            )
        )

        summary = self._build_summary(checks)

        overall_status = summary.overall_status

        processing_status = (
            "approved"
            if overall_status == "passed"
            else "review"
        )

        source = QAReportSource(
            production_plan_id=production_plan.production_plan_id,
            storyboard_id=production_plan.source.storyboard_id,
            asset_plan_id=production_plan.source.asset_plan_id,
            voice_plan_id=production_plan.source.voice_plan_id,
            music_sfx_plan_id=production_plan.source.music_sfx_plan_id,
            script_id=production_plan.source.script_id,
            idea_id=production_plan.source.idea_id,
            opportunity_id=production_plan.source.opportunity_id,
            signal_id=production_plan.source.signal_id,
        )

        return QAReport(
            schema_version="1.0",
            qa_report_id=f"qa_report_{production_plan.production_plan_id}",
            created_at=created_at,
            qa_version="1",
            source=source,
            checks=checks,
            summary=summary,
            processing=QAProcessing(
                status=processing_status,
                confidence=1.0,
                processed_at=created_at,
            ),
        )

    @staticmethod
    def _check_production_timeline(production_plan) -> QACheck:
        timeline = production_plan.timeline

        if not timeline:
            return QACheck(
                check_id="check_production_timeline",
                category="production",
                name="Production timeline exists",
                status="failed",
                severity="critical",
                message="Production timeline is empty.",
            )

        return QACheck(
            check_id="check_production_timeline",
            category="production",
            name="Production timeline exists",
            status="passed",
            severity="info",
            message="Production timeline contains scenes.",
        )

    @staticmethod
    def _check_asset_references(
        production_plan,
        asset_plan,
    ) -> QACheck:

        available_asset_ids = {
            asset.asset_id
            for asset in asset_plan.assets
        }

        missing = []

        for item in production_plan.timeline:
            for asset_id in item.asset_ids:
                if asset_id not in available_asset_ids:
                    missing.append(asset_id)

        if missing:
            return QACheck(
                check_id="check_asset_references",
                category="references",
                name="Asset references",
                status="failed",
                severity="high",
                message=(
                    "Missing asset references: "
                    + ", ".join(sorted(set(missing)))
                ),
            )

        return QACheck(
            check_id="check_asset_references",
            category="references",
            name="Asset references",
            status="passed",
            severity="info",
            message="All production asset references exist.",
        )

    @staticmethod
    def _check_voice_references(
        production_plan,
        voice_plan,
    ) -> QACheck:

        available_voice_ids = {
            segment.segment_id
            for segment in voice_plan.segments
        }

        missing = []

        for item in production_plan.timeline:
            for voice_id in item.voice_segment_ids:
                if voice_id not in available_voice_ids:
                    missing.append(voice_id)

        if missing:
            return QACheck(
                check_id="check_voice_references",
                category="voice",
                name="Voice references",
                status="failed",
                severity="high",
                message=(
                    "Missing voice references: "
                    + ", ".join(sorted(set(missing)))
                ),
            )

        return QACheck(
            check_id="check_voice_references",
            category="voice",
            name="Voice references",
            status="passed",
            severity="info",
            message="All production voice references exist.",
        )

    @staticmethod
    def _check_music_sfx_references(
        production_plan,
        music_sfx_plan,
    ) -> QACheck:

        available_track_ids = {
            track.track_id
            for track in music_sfx_plan.tracks
        }

        missing = []

        for item in production_plan.timeline:
            for track_id in item.music_sfx_track_ids:
                if track_id not in available_track_ids:
                    missing.append(track_id)

        if missing:
            return QACheck(
                check_id="check_music_sfx_references",
                category="audio",
                name="Music and SFX references",
                status="failed",
                severity="high",
                message=(
                    "Missing music/SFX references: "
                    + ", ".join(sorted(set(missing)))
                ),
            )

        return QACheck(
            check_id="check_music_sfx_references",
            category="audio",
            name="Music and SFX references",
            status="passed",
            severity="info",
            message="All production audio references exist.",
        )

    @staticmethod
    def _check_timeline_continuity(production_plan) -> QACheck:
        timeline = production_plan.timeline

        if not timeline:
            return QACheck(
                check_id="check_timeline_continuity",
                category="timeline",
                name="Timeline continuity",
                status="failed",
                severity="critical",
                message="Cannot validate an empty timeline.",
            )

        previous_end = 0.0

        for item in timeline:
            if item.start_time_seconds != previous_end:
                return QACheck(
                    check_id="check_timeline_continuity",
                    category="timeline",
                    name="Timeline continuity",
                    status="failed",
                    severity="high",
                    message=(
                        f"Timeline gap or overlap before "
                        f"{item.timeline_id}."
                    ),
                )

            if item.end_time_seconds <= item.start_time_seconds:
                return QACheck(
                    check_id="check_timeline_continuity",
                    category="timeline",
                    name="Timeline continuity",
                    status="failed",
                    severity="high",
                    message=(
                        f"Invalid duration in {item.timeline_id}."
                    ),
                )

            previous_end = item.end_time_seconds

        return QACheck(
            check_id="check_timeline_continuity",
            category="timeline",
            name="Timeline continuity",
            status="passed",
            severity="info",
            message="Production timeline is continuous and valid.",
        )

    @staticmethod
    def _check_source_references(
        production_plan,
        asset_plan,
        voice_plan,
        music_sfx_plan,
    ) -> QACheck:

        if (
            production_plan.source.asset_plan_id
            != asset_plan.asset_plan_id
        ):
            return QACheck(
                check_id="check_source_references",
                category="references",
                name="Source plan references",
                status="failed",
                severity="high",
                message="Asset plan reference does not match.",
            )

        if (
            production_plan.source.voice_plan_id
            != voice_plan.voice_plan_id
        ):
            return QACheck(
                check_id="check_source_references",
                category="references",
                name="Source plan references",
                status="failed",
                severity="high",
                message="Voice plan reference does not match.",
            )

        if (
            production_plan.source.music_sfx_plan_id
            != music_sfx_plan.music_sfx_plan_id
        ):
            return QACheck(
                check_id="check_source_references",
                category="references",
                name="Source plan references",
                status="failed",
                severity="high",
                message="Music/SFX plan reference does not match.",
            )

        return QACheck(
            check_id="check_source_references",
            category="references",
            name="Source plan references",
            status="passed",
            severity="info",
            message="All source plan references match.",
        )

    @staticmethod
    def _build_summary(checks) -> QASummary:
        passed = sum(
            1 for check in checks
            if check.status == "passed"
        )

        warnings = sum(
            1 for check in checks
            if check.status == "warning"
        )

        failed = sum(
            1 for check in checks
            if check.status == "failed"
        )

        if failed > 0:
            overall_status = "failed"
        elif warnings > 0:
            overall_status = "passed_with_warnings"
        else:
            overall_status = "passed"

        return QASummary(
            overall_status=overall_status,
            total_checks=len(checks),
            passed=passed,
            warnings=warnings,
            failed=failed,
        )