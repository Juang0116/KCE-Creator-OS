import json
from pathlib import Path

from jsonschema import validate

from src.radar.feeds import TECHCRUNCH_MAIN
from src.radar.radar import RadarV0
from src.radar.runner import RadarRunner


def test_real_radar_signal_matches_schema():
    schema_path = (
        Path(__file__).resolve().parents[1]
        / "schemas"
        / "radar_signal.schema.json"
    )

    with schema_path.open("r", encoding="utf-8") as file:
        schema = json.load(file)

    runner = RadarRunner(
        feeds=[TECHCRUNCH_MAIN],
        radar=RadarV0(),
    )

    signals = runner.run()

    assert signals

    for signal in signals:
        validate(
            instance=signal.to_dict(),
            schema=schema,
        )