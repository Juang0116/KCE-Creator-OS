from src.radar.sources import (
    ManualRadarSource,
    RadarSource,
)


def test_manual_radar_source_returns_raw_signals():
    raw_signals = [
        {
            "title": "Nueva GPU",
            "summary": "Nueva GPU para creadores.",
            "source_type": "manual",
            "platform": "test",
        },
        {
            "title": "Nuevo juego",
            "summary": "Nueva actualización.",
            "source_type": "manual",
            "platform": "test",
        },
    ]

    source = ManualRadarSource(
        raw_signals=raw_signals
    )

    result = source.fetch()

    assert result == raw_signals


def test_manual_radar_source_returns_copy():
    raw_signals = [
        {
            "title": "Nueva GPU",
            "summary": "Nueva GPU para creadores.",
        }
    ]

    source = ManualRadarSource(
        raw_signals=raw_signals
    )

    result = source.fetch()

    assert result is not raw_signals
    assert result == raw_signals


def test_manual_radar_source_satisfies_radar_source_contract():
    source: RadarSource = ManualRadarSource(
        raw_signals=[]
    )

    assert source.fetch() == []


def test_manual_radar_source_defaults_to_empty():
    source = ManualRadarSource()

    assert source.fetch() == []