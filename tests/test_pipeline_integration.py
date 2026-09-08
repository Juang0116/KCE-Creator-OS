from src.radar.radar import RadarV0
from src.brand_brain.brain import BrandBrainV0
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


def test_full_content_pipeline_v0():
    # ---------------------------------------------------------
    # 1. BRAND
    # ---------------------------------------------------------
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
            "primary_platforms": [
                "YouTube",
            ],
        },
    }

    # ---------------------------------------------------------
    # 2. RADAR
    # ---------------------------------------------------------
    raw_signals = [
        {
            "title": "Nueva generación de inteligencia artificial",
            "summary": (
                "Una nueva tecnología de inteligencia artificial "
                "está generando interés entre usuarios."
            ),
            "source": "test_source",
            "source_type": "test",
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

    radar = RadarV0()
    signals = radar.collect(raw_signals)

    assert signals
    signal = signals[0]

    # ---------------------------------------------------------
    # 3. BRAND BRAIN
    # ---------------------------------------------------------
    brand_brain = BrandBrainV0()
    brand_evaluation = brand_brain.evaluate(signal, brand)

    assert brand_evaluation.relevant is True
    assert brand_evaluation.relevance_score > 0

    # ---------------------------------------------------------
    # 4. OPPORTUNITY
    # ---------------------------------------------------------
    opportunity_engine = OpportunityEngineV0()

    opportunity = opportunity_engine.evaluate(
        signal,
        brand,
        brand_evaluation,
    )

    assert opportunity
    assert opportunity.scoring.total_score >= 0
    assert opportunity.scoring.total_score <= 100

    # ---------------------------------------------------------
    # 5. CONTENT IDEA
    # ---------------------------------------------------------
    idea_engine = ContentIdeaEngineV0()

    idea = idea_engine.generate(
        opportunity,
        brand,
    )

    assert idea
    assert idea.idea_id
    assert idea.opportunity_id == opportunity.opportunity_id

    # ---------------------------------------------------------
    # 6. RESEARCH
    # ---------------------------------------------------------
    research_engine = ResearchEngineV0()

    research = research_engine.generate(
        idea,
        brand,
    )

    assert research
    assert research.idea_id == idea.idea_id
    assert research.opportunity_id == opportunity.opportunity_id

    # ---------------------------------------------------------
    # 7. FACT CHECK
    # ---------------------------------------------------------
    fact_check_engine = FactCheckEngineV0()

    fact_check = fact_check_engine.generate(
        research,
    )

    assert fact_check
    assert fact_check.research_id == research.research_id

    # ---------------------------------------------------------
    # 8. SCRIPT
    # ---------------------------------------------------------
    script_engine = ScriptEngineV0()

    script = script_engine.generate(
        idea,
        research,
        fact_check,
    )

    assert script
    assert script.script_id
    assert script.source.idea_id == idea.idea_id

    # ---------------------------------------------------------
    # 9. VOICE
    # ---------------------------------------------------------
    voice_profile = VoiceProfile(
        voice_id="futuro_tech_voice_01",
        language="es",
        tone="educativo",
        style="claro_y_dinamico",
        gender="neutral",
        age_range="adult",
    )

    voice_engine = VoiceEngineV0()

    voice_plan = voice_engine.generate(
        script,
        voice_profile,
    )

    assert voice_plan
    assert voice_plan.voice_plan_id
    assert voice_plan.source.script_id == script.script_id

    # ---------------------------------------------------------
    # 10. STORYBOARD
    # ---------------------------------------------------------
    storyboard_engine = StoryboardEngineV0()

    storyboard = storyboard_engine.generate(
        script,
    )

    assert storyboard
    assert storyboard.storyboard_id
    assert storyboard.source.script_id == script.script_id
    assert storyboard.scenes

    # ---------------------------------------------------------
    # 11. ASSETS
    # ---------------------------------------------------------
    asset_engine = AssetEngineV0()

    asset_plan = asset_engine.generate(
        storyboard,
    )

    assert asset_plan
    assert asset_plan.asset_plan_id

    # ---------------------------------------------------------
    # 12. MUSIC / SFX
    # ---------------------------------------------------------
    music_sfx_engine = MusicSFXEngineV0()

    music_sfx_plan = music_sfx_engine.generate(
        storyboard,
    )

    assert music_sfx_plan
    assert music_sfx_plan.music_sfx_plan_id

    # ---------------------------------------------------------
    # 13. PRODUCTION
    # ---------------------------------------------------------
    production_engine = ProductionEngineV0()

    production_plan = production_engine.generate(
        storyboard,
        asset_plan,
        voice_plan,
        music_sfx_plan,
    )

    assert production_plan
    assert production_plan.production_plan_id
    assert production_plan.timeline

    # ---------------------------------------------------------
    # 14. QA
    # ---------------------------------------------------------
    qa_engine = QAEngineV0()

    qa_report = qa_engine.generate(
        production_plan,
        asset_plan,
        voice_plan,
        music_sfx_plan,
    )

    assert qa_report
    assert qa_report.qa_report_id

    # ---------------------------------------------------------
    # 15. THUMBNAIL
    # ---------------------------------------------------------
    thumbnail_engine = ThumbnailEngineV0()

    thumbnail_plan = thumbnail_engine.generate(
        production_plan,
    )

    assert thumbnail_plan
    assert thumbnail_plan.thumbnail_plan_id

    # ---------------------------------------------------------
    # 16. METADATA
    # ---------------------------------------------------------
    metadata_engine = MetadataEngineV0()

    metadata_plan = metadata_engine.generate(
        thumbnail_plan,
    )

    assert metadata_plan
    assert metadata_plan.metadata_plan_id

    # ---------------------------------------------------------
    # 17. APPROVAL
    # ---------------------------------------------------------
    approval_engine = ApprovalEngineV0()

    approval_plan = approval_engine.generate(
        production_plan,
        qa_report,
        thumbnail_plan,
        metadata_plan,
    )

    assert approval_plan
    assert approval_plan.approval_id

    # Approval Engine V0 correctly requires human approval.
    assert approval_plan.decision.status == "pending"

    # ---------------------------------------------------------
    # 18. SIMULATE HUMAN APPROVAL
    # ---------------------------------------------------------
    approval_plan.decision.status = "approved"

    # ---------------------------------------------------------
    # 19. PUBLISH
    # ---------------------------------------------------------
    publish_engine = PublishEngineV0()

    publish_plan = publish_engine.generate(
        approval_plan,
        production_plan,
        thumbnail_plan,
        metadata_plan,
    )

    assert publish_plan
    assert publish_plan.publish_plan_id
    assert publish_plan.publication.status == "ready"

    # ---------------------------------------------------------
    # 20. ANALYTICS
    # ---------------------------------------------------------
    analytics_engine = AnalyticsEngineV0()

    analytics_record = analytics_engine.generate(
        publish_plan,
        content_id="test_content_001",
        metrics={
            "views": 10000,
            "impressions": 50000,
            "ctr": 0.12,
            "watch_time_seconds": 60000,
            "average_view_duration_seconds": 60,
            "likes": 700,
            "comments": 80,
            "shares": 120,
            "subscribers_gained": 150,
            "revenue": 25.0,
        },
    )

    assert analytics_record
    assert analytics_record.analytics_id
    assert analytics_record.target.content_id == "test_content_001"

    # ---------------------------------------------------------
    # 21. LEARNING
    # ---------------------------------------------------------
    learning_engine = LearningEngineV0()

    learning_record = learning_engine.generate(
        analytics_record,
    )

    assert learning_record
    assert learning_record.learning_id
    assert learning_record.source.analytics_id == analytics_record.analytics_id

    # ---------------------------------------------------------
    # 22. FEEDBACK
    # ---------------------------------------------------------
    feedback_engine = FeedbackEngineV0()

    feedback_record = feedback_engine.generate(
        learning_record,
    )

    assert feedback_record
    assert feedback_record.feedback_id
    assert feedback_record.source.learning_id == learning_record.learning_id

    # ---------------------------------------------------------
    # FINAL GENEALOGY CHECK
    # ---------------------------------------------------------
    assert (
        feedback_record.source.learning_id
        == learning_record.learning_id
    )

    assert (
        learning_record.source.analytics_id
        == analytics_record.analytics_id
    )

    assert (
        analytics_record.source.publish_plan_id
        == publish_plan.publish_plan_id
    )

    assert (
        publish_plan.source.approval_id
        == approval_plan.approval_id
    )

    assert (
        approval_plan.source.production_plan_id
        == production_plan.production_plan_id
    )

    assert (
        production_plan.source.storyboard_id
        == storyboard.storyboard_id
    )

    assert (
        storyboard.source.script_id
        == script.script_id
    )

    assert (
        script.source.idea_id
        == idea.idea_id
    )

    assert (
        idea.opportunity_id
        == opportunity.opportunity_id
    )

    assert (
        opportunity.signal_id
        == signal.signal_id
    )