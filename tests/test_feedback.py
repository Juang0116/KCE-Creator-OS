from src.analytics.engine import AnalyticsEngineV0
from src.analytics.models import AnalyticsMetrics
from src.learning.engine import LearningEngineV0
from src.feedback.engine import FeedbackEngineV0


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
    publish_plan_id = "publish_001"
    source = MockSource()
    target = MockTarget()


def create_learning(metrics):
    analytics_engine = AnalyticsEngineV0()

    analytics = analytics_engine.generate(
        publish_plan=MockPublishPlan(),
        content_id="content_001",
        metrics=metrics,
    )

    learning_engine = LearningEngineV0()
    return learning_engine.generate(analytics)


def test_strong_ctr_generates_reinforce_action():
    learning = create_learning(
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
            revenue=0.0,
        )
    )

    engine = FeedbackEngineV0()
    result = engine.generate(learning)

    assert len(result.actions) >= 1
    assert result.actions[0].type == "reinforce"
    assert result.actions[0].priority == "high"
    assert result.actions[0].status == "proposed"


def test_weak_ctr_generates_review_action():
    learning = create_learning(
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

    engine = FeedbackEngineV0()
    result = engine.generate(learning)

    assert len(result.actions) >= 1
    assert result.actions[0].type == "review"
    assert result.actions[0].priority == "high"
    assert result.actions[0].status == "proposed"


def test_audience_learning_generates_experiment_action():
    learning = create_learning(
        AnalyticsMetrics(
            views=1000,
            impressions=10000,
            ctr=0.05,
            watch_time_seconds=5000.0,
            average_view_duration_seconds=300.0,
            likes=60,
            comments=5,
            shares=5,
            subscribers_gained=10,
            revenue=0.0,
        )
    )

    engine = FeedbackEngineV0()
    result = engine.generate(learning)

    audience_actions = [
        action
        for action in result.actions
        if action.type == "experiment"
    ]

    assert len(audience_actions) >= 1
    assert audience_actions[0].priority == "high"
    assert audience_actions[0].status == "proposed"
