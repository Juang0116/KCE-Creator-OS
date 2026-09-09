from src.integrations.notion import (
    FakeNotionClient,
    NotionDiscoveryMapper,
    NotionDiscoveryRepository,
)
from src.orchestration import DiscoveryWorkflowV0

from tests.test_discovery import (
    make_brand,
    make_signal,
)


def make_package():
    return DiscoveryWorkflowV0().run(
        signal=make_signal(),
        brand=make_brand(),
    )


def test_notion_mapper_creates_properties():
    package = make_package()

    mapper = NotionDiscoveryMapper()

    properties = mapper.map(package)

    assert "Name" in properties
    assert "Status" in properties
    assert "Channel" in properties
    assert "Platform" in properties

    assert (
        properties["Status"]["select"]["name"]
        == "Pendiente de Revisión"
    )


def test_notion_mapper_preserves_lineage():
    package = make_package()

    properties = NotionDiscoveryMapper().map(
        package
    )

    assert (
        properties["Discovery ID"]["rich_text"][0]["text"]["content"]
        == package.discovery.discovery_id
    )

    assert (
        properties["Signal ID"]["rich_text"][0]["text"]["content"]
        == package.discovery.signal.signal_id
    )

    assert (
        properties["Opportunity ID"]["rich_text"][0]["text"]["content"]
        == package.discovery.opportunity.opportunity_id
    )

    assert (
        properties["Idea ID"]["rich_text"][0]["text"]["content"]
        == package.discovery.idea.idea_id
    )

    assert (
        properties["Approval ID"]["rich_text"][0]["text"]["content"]
        == package.approval.approval_id
    )


def test_notion_mapper_maps_high_score_to_high_priority():
    package = make_package()

    package.discovery.opportunity.scoring.total_score = 75

    properties = NotionDiscoveryMapper().map(
        package
    )

    assert (
        properties["Priority"]["select"]["name"]
        == "High"
    )


def test_notion_mapper_maps_strong_score_to_critical():
    package = make_package()

    package.discovery.opportunity.scoring.total_score = 85

    properties = NotionDiscoveryMapper().map(
        package
    )

    assert (
        properties["Priority"]["select"]["name"]
        == "Critical"
    )


def test_notion_fake_client_creates_page():
    package = make_package()

    client = FakeNotionClient()

    repository = NotionDiscoveryRepository(
        client=client
    )

    result = repository.create(
        package=package,
        database_id="content_factory_001",
    )

    assert result["id"] == "fake_page_001"

    assert (
        result["database_id"]
        == "content_factory_001"
    )

    assert len(client.created_pages) == 1


def test_notion_repository_preserves_mapped_properties():
    package = make_package()

    client = FakeNotionClient()

    repository = NotionDiscoveryRepository(
        client=client
    )

    result = repository.create(
        package=package,
        database_id="content_factory_001",
    )

    properties = result["properties"]

    assert (
        properties["Discovery ID"]["rich_text"][0]["text"]["content"]
        == package.discovery.discovery_id
    )

    assert (
        properties["Approval ID"]["rich_text"][0]["text"]["content"]
        == package.approval.approval_id
    )


def test_notion_fake_client_updates_page():
    package = make_package()

    client = FakeNotionClient()

    repository = NotionDiscoveryRepository(
        client=client
    )

    result = repository.update(
        package=package,
        page_id="page_existing_001",
    )

    assert (
        result["id"]
        == "page_existing_001"
    )

    assert len(client.updated_pages) == 1


def test_notion_mapper_rejects_missing_idea():
    package = make_package()

    package.discovery.idea = None

    try:
        NotionDiscoveryMapper().map(
            package
        )
    except ValueError as exc:
        assert (
            "without a ContentIdea"
            in str(exc)
        )
    else:
        raise AssertionError(
            "Expected ValueError"
        )


def test_notion_mapper_rejects_missing_approval():
    package = make_package()

    package.approval = None

    try:
        NotionDiscoveryMapper().map(
            package
        )
    except ValueError as exc:
        assert (
            "without a DiscoveryApproval"
            in str(exc)
        )
    else:
        raise AssertionError(
            "Expected ValueError"
        )