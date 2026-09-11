from fastapi.testclient import TestClient

from src.api.app import app
from src.application import (
    DiscoveryApplicationServiceV0,
    DiscoveryFacadeV0,
    DiscoveryQueryServiceV0,
)
from src.api.dependencies import get_discovery
from src.persistence import (
    DiscoveryPackageRepository,
    MemoryRepository,
)
from src.orchestration import DiscoveryWorkflowV0

from tests.test_discovery import (
    make_brand,
    make_signal,
)


def make_test_facade() -> DiscoveryFacadeV0:
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


def make_client(facade: DiscoveryFacadeV0) -> TestClient:
    app.dependency_overrides[get_discovery] = (
        lambda: facade
    )

    return TestClient(app)


def cleanup_dependencies() -> None:
    app.dependency_overrides.clear()


def test_health_endpoint():
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
    }


def test_post_discovery_returns_created_package():
    facade = make_test_facade()
    client = make_client(facade)

    try:
        response = client.post(
            "/discovery",
            json={
                "signal": make_signal().to_dict(),
                "brand": make_brand(),
            },
        )
    finally:
        cleanup_dependencies()

    assert response.status_code == 201

    body = response.json()

    assert "discovery" in body
    assert "approval" in body

    assert (
        body["discovery"]["signal"]["signal_id"]
        == "sig_discovery_001"
    )


def test_get_discovery_returns_package():
    facade = make_test_facade()

    package = facade.run(
        signal=make_signal(),
        brand=make_brand(),
    )

    client = make_client(facade)

    try:
        response = client.get(
            f"/discovery/{package.discovery.discovery_id}"
        )
    finally:
        cleanup_dependencies()

    assert response.status_code == 200

    body = response.json()

    assert (
        body["discovery"]["discovery_id"]
        == package.discovery.discovery_id
    )


def test_get_missing_discovery_returns_404():
    facade = make_test_facade()
    client = make_client(facade)

    try:
        response = client.get(
            "/discovery/discovery_missing"
        )
    finally:
        cleanup_dependencies()

    assert response.status_code == 404

    assert response.json()["detail"] == (
        "Discovery not found."
    )


def test_list_discoveries_returns_packages():
    facade = make_test_facade()

    package_1 = facade.run(
        signal=make_signal(),
        brand=make_brand(),
    )

    package_2 = facade.run(
        signal=make_signal(),
        brand=make_brand(),
    )

    client = make_client(facade)

    try:
        response = client.get("/discovery")
    finally:
        cleanup_dependencies()

    assert response.status_code == 200

    body = response.json()

    assert len(body["discoveries"]) == 2

    ids = {
        discovery["discovery_id"]
        for discovery in body["discoveries"]
    }

    assert package_1.discovery.discovery_id in ids
    assert package_2.discovery.discovery_id in ids