from src.analytics.engine import AnalyticsEngineV0
from src.analytics.models import AnalyticsMetrics
from src.learning.engine import LearningEngineV0


class MockSource:
    publish_plan_id = "publish_001"
    approval_id = "approval_001"
    production_plan_id = "production_001"
    thumbnail_plan_id = "thumbnail_001"
    metadata_plan_id = "metadata_001"
    storyboard_id = "storyboard_001"
    script_id = "script_001"
    idea_id = "idea_001"
    opportunity_id = "opportunity_001"
    signal_id = "signal_001"


class MockTarget:
    brand_id = "brand_001"
    channel = "Futuro Tech"
    platform = "YouTube"


class MockPublishPlan:
    publish_id = "publish_001"
    source = MockSource()
    target = MockTarget()


def create_analytics(metrics):
    analytics_engine = AnalyticsEngineV0()

    return analytics_engine.generate(
        publish_plan=MockPublishPlan(),
        content_id="content_001",
        metrics=metrics,
    )


def test_generate_strong_ctr_learning():
    analytics = create_analytics(
        AnalyticsMetrics(
            views=5000,
            impressions=10000,
            ctr=0.12,
            watch_time_seconds=20000.0,
            average_view_duration_seconds=240.0,
            likes=200,
            comments=30,
            shares=40,
            subscribers_gained=50,
            revenue=10.0,
        )
    )

    engine = LearningEngineV0()
    result = engine.generate(analytics)

    assert result.learning_id == "learning_content_001"
    assert result.processing.status == "generated"
    assert len(result.insights) >= 1
    assert result.insights[0].category == "performance"


def test_generate_weak_ctr_learning():
    analytics = create_analytics(
        AnalyticsMetrics(
            views=1000,
            impressions=10000,
            ctr=0.02,
            watch_time_seconds=3000.0,
            average_view_duration_seconds=180.0,
            likes=20,
            comments=2,
            shares=3,
            subscribers_gained=5,
            revenue=0.0,
        )
    )

    engine = LearningEngineV0()
    result = engine.generate(analytics)

    assert len(result.insights) >= 1
    assert result.insights[0].insight_id == "insight_ctr_weak"
    assert result.insights[0].category == "performance"


def test_generate_fallback_learning():
    analytics = create_analytics(
        AnalyticsMetrics(
            views=100,
            impressions=1000,
            ctr=0.05,
            watch_time_seconds=500.0,
            average_view_duration_seconds=120.0,
            likes=1,
            comments=0,
            shares=0,
            subscribers_gained=0,
            revenue=0.0,
        )
    )

    engine = LearningEngineV0()
    result = engine.generate(analytics)

    assert len(result.insights) == 1
    assert result.insights[0].insight_id == "insight_insufficient_signal"
    assert result.insights[0].confidence == 0.5
    