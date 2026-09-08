from src.voice.engine import VoiceEngineV0
from src.voice.models import VoiceProfile
from src.script.models import (
    ScriptSource,
    ScriptTarget,
    ScriptHook,
    ScriptIntroduction,
    ScriptSection,
    ScriptConclusion,
    ScriptCTA,
)


class MockScript:
    script_id = "script_001"

    source = ScriptSource(
        idea_id="idea_001",
        research_id="research_001",
        fact_check_id="fact_check_001",
        opportunity_id="opportunity_001",
        signal_id="signal_001",
    )

    target = ScriptTarget(
        brand_id="brand_001",
        channel="Futuro Tech",
        platform="youtube",
    )

    hook = ScriptHook(
        narration="La tecnología está cambiando nuestra forma de crear.",
        visual_direction="Show technology examples.",
    )

    introduction = ScriptIntroduction(
        narration="Hoy vamos a descubrir cómo funciona este cambio.",
        visual_direction="Introduce the topic.",
    )

    sections = [
        ScriptSection(
            section_id="section_001",
            title="El cambio",
            narration="Las nuevas herramientas permiten producir contenido más rápido.",
            claims=[],
            visual_direction="Show technology examples.",
            transition="Continue.",
        ),
        ScriptSection(
            section_id="section_002",
            title="El futuro",
            narration="El futuro será una combinación entre creatividad humana e inteligencia artificial.",
            claims=[],
            visual_direction="Show futuristic creator workflow.",
            transition="Final transition.",
        ),
    ]

    conclusion = ScriptConclusion(
        narration="La tecnología no reemplaza la creatividad: la amplifica.",
        visual_direction="Show final creator workflow.",
    )

    cta = ScriptCTA(
        narration="Suscríbete para aprender más.",
        visual_direction="Show subscribe CTA.",
    )


def test_voice_engine_v0_generates_valid_voice_plan():
    engine = VoiceEngineV0()

    voice_profile = VoiceProfile(
        voice_id="voice_futuro_tech",
        language="es",
        tone="professional",
        style="educational",
        gender="neutral",
        age_range="adult",
    )

    script = MockScript()

    voice_plan = engine.generate(
        script,
        voice_profile,
    )

    assert voice_plan.voice_plan_id == "voice_plan_script_001"
    assert voice_plan.schema_version == "1.0"
    assert voice_plan.voice_plan_version == "1"
    assert voice_plan.target.channel == "Futuro Tech"
    assert voice_plan.target.platform == "youtube"
    assert len(voice_plan.segments) == 6
    assert voice_plan.processing.status == "draft"


def test_voice_engine_preserves_script_references():
    engine = VoiceEngineV0()

    voice_profile = VoiceProfile(
        voice_id="voice_futuro_tech",
        language="es",
        tone="professional",
        style="educational",
        gender="neutral",
        age_range="adult",
    )

    script = MockScript()

    voice_plan = engine.generate(
        script,
        voice_profile,
    )

    assert voice_plan.source.script_id == "script_001"
    assert voice_plan.source.idea_id == "idea_001"
    assert voice_plan.source.opportunity_id == "opportunity_001"
    assert voice_plan.source.signal_id == "signal_001"


def test_voice_plan_to_dict_contains_expected_structure():
    engine = VoiceEngineV0()

    voice_profile = VoiceProfile(
        voice_id="voice_futuro_tech",
        language="es",
        tone="professional",
        style="educational",
        gender="neutral",
        age_range="adult",
    )

    script = MockScript()

    voice_plan = engine.generate(
        script,
        voice_profile,
    )

    data = voice_plan.to_dict()

    assert "schema_version" in data
    assert "voice_plan_id" in data
    assert "source" in data
    assert "target" in data
    assert "voice_profile" in data
    assert "segments" in data
    assert "processing" in data