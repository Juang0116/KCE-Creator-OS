import json
from pathlib import Path

from jsonschema import Draft202012Validator

from src.radar import RadarV0


def test_radar_signal_matches_schema():
    radar = RadarV0()

    raw_signal = {
        "title": "Nueva GPU para creadores",
        "summary": (
            "Una nueva GPU promete mejorar el rendimiento "
            "de aplicaciones de IA y creación de contenido."
        ),
        "source_type": "news",
        "platform": "TechNews",
        "keywords": ["GPU", "IA", "creadores"],
        "topics": ["technology", "AI"],
        "language": "es",
        "niches": ["technology", "AI"],
        "relevance_reason": "Puede ser relevante para Futuro Tech",
    }

    signals = radar.collect([raw_signal])
    signal_data = signals[0].to_dict()

    schema_path = (
        Path(__file__).parent.parent
        / "schemas"
        / "radar_signal.schema.json"
    )

    with open(schema_path, "r", encoding="utf-8") as file:
        schema = json.load(file)

    validator = Draft202012Validator(schema)

    errors = list(validator.iter_errors(signal_data))

    assert not errors, "\n".join(
        error.message for error in errors
    )