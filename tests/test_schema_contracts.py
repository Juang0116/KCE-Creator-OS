import json
from pathlib import Path

from jsonschema import Draft202012Validator

from src.radar.radar import RadarV0
from src.opportunity.engine import OpportunityEngineV0
from src.content.ideas.engine import ContentIdeaEngineV0
from src.research.engine import ResearchEngineV0
from src.fact_check.engine import FactCheckEngineV0
from src.script.engine import ScriptEngineV0
from src.voice.engine import VoiceEngineV0
from src.voice.models import VoiceProfile
from src.storyboard.engine import StoryboardEngineV0
from src.asset.engine import AssetEngineV0
from src.music_sfx.engine import MusicSFXEngineV0
from src.production.engine import ProductionEngineV0
from src.qa.engine import QAEngineV0
from src.thumbnail.engine import ThumbnailEngineV0
from src.metadata.engine import MetadataEngineV0
from src.approval.engine import ApprovalEngineV0
from src.publish.engine import PublishEngineV0
from src.analytics.engine import AnalyticsEngineV0
from src.learning.engine import LearningEngineV0
from src.feedback.engine import FeedbackEngineV0


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"


def load_schema(name):
    path = SCHEMA_DIR / f"{name}.schema.json"

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def assert_matches_schema(name, artifact):
    schema = load_schema(name)
    validator = Draft202012Validator(schema)

    errors = sorted(
        validator.iter_errors(artifact),
        key=lambda error: list(error.path),
    )

    if errors:
        details = "\n".join(
            f"- {error.json_path}: {error.message}"
            for error in errors
        )

        raise AssertionError(
            f"{name}.schema.json rejected the generated artifact:\n"
            f"{details}"
        )


def build_pipeline_artifacts():
    brand = {
        "brand_id": "futuro_tech",
        "identity": {
            "name": "Futuro Tech",
            "mission": "Explicar tecnología de forma clara y útil.",
        },
        "audience": {
            "target": "Personas interesadas en tecnología",
            "age": "18-40",
        },
        "personality": {
            "archetype": "Explorer",
            "tone": "Claro, curioso y profesional",
            "voice": "Educativo",
        },
        "content": {
            "pillars": [
                "tecnologia",
                "inteligencia artificial",
                "futuro",
            ],
            "topics": [
                "IA",
                "software",
                "hardware",
                "innovacion",
            ],
        },
        "channels_community": {
            "primary_platforms": ["YouTube"],
        },
    }

    raw_signals = [
        {
            "title": "Nueva generación de inteligencia artificial",
            "summary": (
                "Una nueva tecnología de inteligencia artificial "
                "está generando interés entre usuarios."
            ),
            "source": "test_source",
            "source_type": "other",
            "url": "https://example.com/test",
            "language": "es",
            "topics": [
                "inteligencia artificial",
                "tecnologia",
                "innovacion",
            ],
            "keywords": [
                "IA",
                "tecnologia",
                "futuro",
            ],
        }
    ]

    # RADAR
    signal = RadarV0().collect(raw_signals)[0]

    # OPPORTUNITY
    opportunity = OpportunityEngineV0().evaluate(
        signal,
        brand,
        _brand_evaluation(signal, brand),
    )

    # CONTENT IDEA
    idea = ContentIdeaEngineV0().generate(
        opportunity,
        brand,
    )

    # RESEARCH
    research = ResearchEngineV0().generate(
        idea,
        brand,
    )

    # FACT CHECK
    fact_check = FactCheckEngineV0().generate(
        research,
    )

    # SCRIPT
    script = ScriptEngineV0().generate(
        idea,
        research,
        fact_check,
    )

    # VOICE
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

    # STORYBOARD
    storyboard = StoryboardEngineV0().generate(
        script,
    )

    # ASSETS
    asset_plan = AssetEngineV0().generate(
        storyboard,
    )

    # MUSIC / SFX
    music_sfx_plan = MusicSFXEngineV0().generate(
        storyboard,
    )

    # PRODUCTION
    production_plan = ProductionEngineV0().generate(
        storyboard,
        asset_plan,
        voice_plan,
        music_sfx_plan,
    )

    # QA
    qa_report = QAEngineV0().generate(
        production_plan,
        asset_plan,
        voice_plan,
        music_sfx_plan,
    )

    # THUMBNAIL
    thumbnail_plan = ThumbnailEngineV0().generate(
        production_plan,
    )

    # METADATA
    metadata_plan = MetadataEngineV0().generate(
        thumbnail_plan,
    )

    # APPROVAL
    approval_plan = ApprovalEngineV0().generate(
        production_plan,
        qa_report,
        thumbnail_plan,
        metadata_plan,
    )

    # PUBLISH
    approval_plan.decision.status = "approved"

    publish_plan = PublishEngineV0().generate(
        approval_plan,
        production_plan,
        thumbnail_plan,
        metadata_plan,
    )

    # ANALYTICS
    analytics_record = AnalyticsEngineV0().generate(
        publish_plan,
        content_id="content_001",
    )

    # LEARNING
    learning_record = LearningEngineV0().generate(
        analytics_record,
    )

    # FEEDBACK
    feedback_record = FeedbackEngineV0().generate(
        learning_record,
    )

    return {
        "radar_signal": signal,
        "opportunity": opportunity,
        "content_idea": idea,
        "research_brief": research,
        "fact_check": fact_check,
        "script": script,
        "voice": voice_plan,
        "storyboard": storyboard,
        "asset": asset_plan,
        "music_sfx": music_sfx_plan,
        "production": production_plan,
        "qa": qa_report,
        "thumbnail": thumbnail_plan,
        "metadata": metadata_plan,
        "approval": approval_plan,
        "publish": publish_plan,
        "analytics": analytics_record,
        "learning": learning_record,
        "feedback": feedback_record,
    }


def _brand_evaluation(signal, brand):
    from src.brand_brain.brain import BrandBrainV0

    return BrandBrainV0().evaluate(
        signal,
        brand,
    )


def test_all_generated_artifacts_match_their_schemas():
    artifacts = build_pipeline_artifacts()

    expected_schemas = {
        "radar_signal": "radar_signal",
        "opportunity": "opportunity",
        "content_idea": "content_idea",
        "research_brief": "research_brief",
        "fact_check": "fact_check",
        "script": "script",
        "voice": "voice",
        "storyboard": "storyboard",
        "asset": "asset",
        "music_sfx": "music_sfx",
        "production": "production",
        "qa": "qa",
        "thumbnail": "thumbnail",
        "metadata": "metadata",
        "approval": "approval",
        "publish": "publish",
        "analytics": "analytics",
        "learning": "learning",
        "feedback": "feedback",
    }

    assert len(expected_schemas) == 19

    failures = []

    for artifact_name, schema_name in expected_schemas.items():
        artifact = artifacts[artifact_name]

        if not hasattr(artifact, "to_dict"):
            failures.append(
                f"{artifact_name}: does not expose to_dict()"
            )
            print(f"FAIL  {artifact_name}")
            continue

        try:
            assert_matches_schema(
                schema_name,
                artifact.to_dict(),
            )
            print(f"PASS  {artifact_name}")
        except AssertionError as exc:
            failures.append(str(exc))
            print(f"FAIL  {artifact_name}")

    if failures:
        raise AssertionError(
            "\n\n".join(
                [
                    "SCHEMA CONTRACT AUDIT FAILED",
                    *failures,
                ]
            )
        )