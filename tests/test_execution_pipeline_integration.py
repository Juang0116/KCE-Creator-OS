from types import SimpleNamespace

from src.asset.engine import AssetEngineV0
from src.execution.engine import ExecutionEngineV0
from src.music_sfx.engine import MusicSFXEngineV0
from src.script.models import (
    Script,
    ScriptClaim,
    ScriptConclusion,
    ScriptCTA,
    ScriptHook,
    ScriptIntroduction,
    ScriptMetadata,
    ScriptProcessing,
    ScriptSection,
    ScriptSource,
    ScriptTarget,
)
from src.storyboard.engine import StoryboardEngineV0
from src.voice.engine import VoiceEngineV0
from src.voice.models import VoiceProfile


def make_script():
    return Script(
        schema_version="1.0",
        script_id="script_integration_001",
        created_at="2026-09-09T00:00:00+00:00",
        script_version="1",
        source=ScriptSource(
            idea_id="idea_integration_001",
            research_id="research_integration_001",
            fact_check_id="fact_integration_001",
            opportunity_id="opportunity_integration_001",
            signal_id="signal_integration_001",
        ),
        target=ScriptTarget(
            brand_id="futuro_tech",
            channel="Futuro Tech",
            platform="YouTube",
        ),
        metadata=ScriptMetadata(
            title="Integration Test",
            format="long_form",
            estimated_duration_seconds=60,
            content_pillar="Technology",
            tone="Educational",
        ),
        hook=ScriptHook(
            narration="La tecnología está cambiando rápidamente.",
            visual_direction="Opening technology montage.",
        ),
        introduction=ScriptIntroduction(
            narration="En este video exploramos estos cambios.",
            visual_direction="Introduce the topic with supporting visuals.",
        ),
        sections=[
            ScriptSection(
                section_id="section_001",
                title="Technology Changes",
                narration="La tecnología transforma la manera en que trabajamos.",
                claims=[
                    ScriptClaim(
                        claim="La tecnología transforma procesos de trabajo.",
                        fact_check_id="fact_integration_001",
                        verification_status="verified",
                    )
                ],
                visual_direction="Show technology and workplace visuals.",
                transition="fade",
            )
        ],
        conclusion=ScriptConclusion(
            narration="Estos cambios seguirán evolucionando.",
            visual_direction="Closing summary visual.",
        ),
        cta=ScriptCTA(
            narration="Suscríbete para más contenido.",
            visual_direction="End screen.",
        ),
        processing=ScriptProcessing(
            status="draft",
            confidence=1.0,
            processed_at=None,
        ),
    )


def test_execution_integrates_real_production_artifacts():
    script = make_script()

    storyboard = StoryboardEngineV0().generate(script)

    voice_profile = VoiceProfile(
        voice_id="futuro_tech_voice_01",
        language="es",
        tone="educativo",
        style="claro_y_dinamico",
        gender="neutral",
        age_range="adult",
    )

    voice_plan = VoiceEngineV0().generate(
        script,
        voice_profile,
    )

    asset_plan = AssetEngineV0().generate(
        storyboard,
    )

    music_sfx_plan = MusicSFXEngineV0().generate(
        storyboard,
    )

    execution = ExecutionEngineV0().run(
        storyboard=storyboard,
        asset_plan=asset_plan,
        voice_plan=voice_plan,
        music_sfx_plan=music_sfx_plan,
    )

    assert execution.status == "awaiting_approval"

    assert execution.lineage.storyboard_id == storyboard.storyboard_id
    assert execution.lineage.script_id == script.script_id
    assert execution.lineage.idea_id == script.source.idea_id
    assert execution.lineage.opportunity_id == script.source.opportunity_id
    assert execution.lineage.signal_id == script.source.signal_id

    stage_names = [stage.name for stage in execution.stages]

    assert stage_names == [
        "production",
        "qa",
        "thumbnail",
        "metadata",
        "approval",
        "publish",
    ]

    assert all(
        stage.status == "completed"
        for stage in execution.stages[:4]
    )

    assert execution.stages[4].status == "waiting"
    assert execution.stages[4].message == "pending"

    assert execution.stages[5].status == "blocked"
    assert execution.stages[5].message == "blocked"
