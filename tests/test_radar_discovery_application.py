from src.application import RadarDiscoveryApplicationServiceV0
from src.radar import RadarV0
from src.radar.sources import ManualRadarSource


class FakeDiscoveryFacade:
    def __init__(self) -> None:
        self.received_signals = []

    def run(self, signal, brand):
        self.received_signals.append(signal)

        return {
            "signal_id": signal.signal_id,
            "brand_id": brand["brand_id"],
        }


def make_raw_signal(title: str, signal_suffix: str) -> dict:
    return {
        "title": title,
        "summary": f"Summary for {title}",
        "source_type": "manual",
        "platform": "test",
        "url": f"https://example.com/{signal_suffix}",
        "author": "tester",
        "published_at": "2026-09-10T12:00:00+00:00",
        "keywords": ["test"],
        "topics": ["technology"],
        "language": "en",
        "evidence": {
            "source": "test",
        },
        "niches": ["technology"],
        "relevance_reason": "Relevant test signal.",
    }


def test_source_is_consumed_by_radar_and_discovery():
    raw_signals = [
        make_raw_signal("Signal One", "one"),
    ]

    source = ManualRadarSource(raw_signals)

    discovery = FakeDiscoveryFacade()
    service = RadarDiscoveryApplicationServiceV0(
        radar=RadarV0(),
        discovery=discovery,
    )

    brand = {
        "brand_id": "brand_test",
    }

    packages = service.run(
        source=source,
        brand=brand,
    )

    assert len(packages) == 1
    assert len(discovery.received_signals) == 1

    signal = discovery.received_signals[0]

    assert signal.title == "Signal One"
    assert signal.platform == "test"


def test_source_can_provide_multiple_signals():
    source = ManualRadarSource(
        [
            make_raw_signal("Signal One", "one"),
            make_raw_signal("Signal Two", "two"),
            make_raw_signal("Signal Three", "three"),
        ]
    )

    discovery = FakeDiscoveryFacade()
    service = RadarDiscoveryApplicationServiceV0(
        radar=RadarV0(),
        discovery=discovery,
    )

    packages = service.run(
        source=source,
        brand={"brand_id": "brand_test"},
    )

    assert len(packages) == 3
    assert len(discovery.received_signals) == 3

    titles = [
        signal.title
        for signal in discovery.received_signals
    ]

    assert titles == [
        "Signal One",
        "Signal Two",
        "Signal Three",
    ]


def test_empty_source_produces_no_discoveries():
    source = ManualRadarSource()

    discovery = FakeDiscoveryFacade()
    service = RadarDiscoveryApplicationServiceV0(
        radar=RadarV0(),
        discovery=discovery,
    )

    packages = service.run(
        source=source,
        brand={"brand_id": "brand_test"},
    )

    assert packages == []
    assert discovery.received_signals == []