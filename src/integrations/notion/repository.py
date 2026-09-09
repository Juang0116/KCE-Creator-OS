from src.orchestration import DiscoveryPackage

from .client import NotionClient
from .mapper import NotionDiscoveryMapper


class NotionDiscoveryRepository:
    """
    Repository for persisting Discovery packages in Notion.
    """

    def __init__(
        self,
        client: NotionClient,
        mapper: NotionDiscoveryMapper | None = None,
    ):
        self.client = client
        self.mapper = (
            mapper
            or NotionDiscoveryMapper()
        )

    def create(
        self,
        package: DiscoveryPackage,
        database_id: str,
    ) -> dict:

        properties = self.mapper.map(
            package
        )

        return self.client.create_page(
            database_id=database_id,
            properties=properties,
        )

    def update(
        self,
        package: DiscoveryPackage,
        page_id: str,
    ) -> dict:

        properties = self.mapper.map(
            package
        )

        return self.client.update_page(
            page_id=page_id,
            properties=properties,
        )