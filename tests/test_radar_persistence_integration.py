from src.radar.feeds import TECHCRUNCH_MAIN
from src.radar.radar import RadarV0
from src.radar.runner import RadarRunner
from src.radar.store import RadarStore


def test_real_radar_pipeline_persists_signals(tmp_path):
    store = RadarStore(
        tmp_path / "radar" / "signals.jsonl"
    )

    runner = RadarRunner(
        feeds=[TECHCRUNCH_MAIN],
        radar=RadarV0(),
    )

    signals = runner.run()

    assert signals

    store.save(signals)

    persisted = store.load()

    assert len(persisted) == len(signals)

    persisted_ids = {
        signal["signal_id"]
        for signal in persisted
    }

    generated_ids = {
        signal.signal_id
        for signal in signals
    }

    assert persisted_ids == generated_ids