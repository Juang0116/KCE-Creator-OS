from src.application import (
    DiscoveryApplicationServiceV0,
    DiscoveryFacadeV0,
    DiscoveryQueryServiceV0,
    RadarDiscoveryApplicationServiceV0,
)
from src.persistence import (
    DiscoveryPackageRepository,
    MemoryRepository,
)
from src.orchestration import DiscoveryWorkflowV0
from src.radar import RadarV0

from tests.test_discovery import make_brand


def make_test_discovery() -> DiscoveryFacadeV0:
    workflow = DiscoveryWorkflowV0()

    memory_repository = MemoryRepository()

    package_repository = DiscoveryPackageRepository(
        repository=memory_repository
    )

    application_service = DiscoveryApplicationServiceV0(
        workflow=workflow,
        package_repository=package_repository,
    )

    query_service = DiscoveryQueryServiceV0(
        package_repository=package_repository,
    )

    return DiscoveryFacadeV0(
        application_service=application_service,
        query_service=query_service,
    )


def make_raw_signal(title: str) -> dict:
    return {
        "title": title,
        "summary": (
            "Una señal de prueba para validar "
            "el circuito Radar hacia Discovery."
        ),
        "source_type": "test",
        "platform": "TestPlatform",
        "url": "https://example.com/test",
        "author": "test_author",
        "published_at": "2026-09-10T00:00:00+00:00",
        "keywords": ["test", "creator_os"],
        "topics": ["technology"],
        "language": "es",
        "evidence": {
            "test": True,
        },
        "niches": ["technology"],
        "relevance_reason": (
            "Señal creada para pruebas."
        ),
        "confidence": 0.9,
    }


def test_radar_discovery_processes_multiple_signals():
    discovery = make_test_discovery()

    service = RadarDiscoveryApplicationServiceV0(
        radar=RadarV0(),
        discovery=discovery,
    )

    raw_signals = [
        make_raw_signal("Señal de prueba 1"),
        make_raw_signal("Señal de prueba 2"),
        make_raw_signal("Señal de prueba 3"),
    ]

    packages = service.run(
        raw_signals=raw_signals,
        brand=make_brand(),
    )

    assert len(packages) == 3

    assert all(
        package.discovery.signal.signal_id
        for package in packages
    )


def test_radar_discovery_persists_each_package():
    discovery = make_test_discovery()

    service = RadarDiscoveryApplicationServiceV0(
        radar=RadarV0(),
        discovery=discovery,
    )

    packages = service.run(
        raw_signals=[
            make_raw_signal("Señal de prueba 1"),
            make_raw_signal("Señal de prueba 2"),
        ],
        brand=make_brand(),
    )

    assert len(discovery.list_all()) == 2

    for package in packages:
        assert discovery.exists(
            package.discovery.discovery_id
        )


def test_radar_discovery_preserves_radar_lineage():
    discovery = make_test_discovery()

    radar = RadarV0()

    service = RadarDiscoveryApplicationServiceV0(
        radar=radar,
        discovery=discovery,
    )

    raw_signals = [
        make_raw_signal("Señal de lineage"),
    ]

    packages = service.run(
        raw_signals=raw_signals,
        brand=make_brand(),
    )

    discovery_signal = packages[0].discovery.signal

    assert discovery_signal.signal_id != ""

    assert (
        discovery_signal.radar_version
        == radar.radar_version
    )

    assert (
        discovery_signal.title
        == "Señal de lineage"
    )