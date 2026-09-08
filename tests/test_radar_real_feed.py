from src.radar.feeds import TECHCRUNCH_MAIN
from src.radar.radar import RadarV0
from src.radar.runner import RadarRunner


def test_radar_runner_reads_real_techcrunch_feed():
    runner = RadarRunner(
        feeds=[TECHCRUNCH_MAIN],
        radar=RadarV0(),
    )

    signals = runner.run()

    assert signals
    assert len(signals) > 0

    first_signal = signals[0]

    assert first_signal.signal_id.startswith("sig_")
    assert first_signal.title
    assert first_signal.summary
    assert first_signal.url
    assert first_signal.source_type == "rss"
    assert first_signal.platform == "rss"
    assert first_signal.status == "detected"