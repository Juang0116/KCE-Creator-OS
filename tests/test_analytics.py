from src.analytics.engine import AnalyticsEngineV0
from src.analytics.models import AnalyticsMetrics


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


def test_generate_analytics_record():
    engine = AnalyticsEngineV0()

    result = engine.generate(
        publish_plan=MockPublishPlan(),
        content_id="content_001",
    )

    assert result.analytics_id == "analytics_content_001"
    assert result.analytics_version == "1"
    assert result.target.brand_id == "brand_001"
    assert result.target.channel == "Futuro Tech"
    assert result.target.platform == "YouTube"
    assert result.target.content_id == "content_001"
    assert result.processing.status == "collected"
    assert result.processing.confidence == 1.0


def test_generate_default_metrics():
    engine = AnalyticsEngineV0()

    result = engine.generate(
        publish_plan=MockPublishPlan(),
        content_id="content_001",
    )

    assert result.metrics.views == 0
    assert result.metrics.impressions == 0
    assert result.metrics.ctr == 0.0
    assert result.metrics.likes == 0
    assert result.metrics.comments == 0
    assert result.metrics.shares == 0
    assert result.metrics.subscribers_gained == 0
    assert result.metrics.revenue == 0.0


def test_generate_custom_metrics():
    engine = AnalyticsEngineV0()

    metrics = AnalyticsMetrics(
        views=1500,
        impressions=10000,
        ctr=0.15,
        watch_time_seconds=7200.0,
        average_view_duration_seconds=288.0,
        likes=120,
        comments=15,
        shares=20,
        subscribers_gained=35,
        revenue=12.50,
    )

    result = engine.generate(
        publish_plan=MockPublishPlan(),
        content_id="content_001",
        metrics=metrics,
    )

    assert result.metrics.views == 1500
    assert result.metrics.impressions == 10000
    assert result.metrics.ctr == 0.15
    assert result.metrics.watch_time_seconds == 7200.0
    assert result.metrics.average_view_duration_seconds == 288.0
    assert result.metrics.likes == 120
    assert result.metrics.comments == 15
    assert result.metrics.shares == 20
    assert result.metrics.subscribers_gained == 35
    assert result.metrics.revenue == 12.50