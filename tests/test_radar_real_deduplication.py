from src.radar.deduplication import RadarDeduplicator
from src.radar.feeds import TECHCRUNCH_MAIN
from src.radar.radar import RadarV0
from src.radar.runner import RadarRunner


def test_real_feed_is_deduplicated_between_runs():
    deduplicator = RadarDeduplicator()

    runner = RadarRunner(
        feeds=[TECHCRUNCH_MAIN],
        radar=RadarV0(),
        deduplicator=deduplicator,
    )

    first_run = runner.run()
    second_run = runner.run()

    assert first_run
    assert second_run == []

    first_ids = {
        signal.signal_id
        for signal in first_run
    }

    assert len(first_ids) == len(first_run)