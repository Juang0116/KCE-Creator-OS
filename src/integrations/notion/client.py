from typing import Any


class NotionClient:
    """
    Minimal Notion client contract.

    V0 defines the interface only.
    A real HTTP implementation will be added later.
    """

    def create_page(
        self,
        database_id: str,
        properties: dict[str, Any],
    ) -> dict[str, Any]:
        raise NotImplementedError(
            "NotionClient.create_page() "
            "must be implemented by a concrete client."
        )

    def update_page(
        self,
        page_id: str,
        properties: dict[str, Any],
    ) -> dict[str, Any]:
        raise NotImplementedError(
            "NotionClient.update_page() "
            "must be implemented by a concrete client."
        )


class FakeNotionClient(NotionClient):
    """
    In-memory Notion client used for tests.

    Does not communicate with Notion.
    """

    def __init__(self):
        self.created_pages = []
        self.updated_pages = []

    def create_page(
        self,
        database_id: str,
        properties: dict[str, Any],
    ) -> dict[str, Any]:

        page_id = (
            f"fake_page_{len(self.created_pages) + 1:03d}"
        )

        page = {
            "id": page_id,
            "database_id": database_id,
            "properties": properties,
        }

        self.created_pages.append(page)

        return page

    def update_page(
        self,
        page_id: str,
        properties: dict[str, Any],
    ) -> dict[str, Any]:

        page = {
            "id": page_id,
            "properties": properties,
        }

        self.updated_pages.append(page)

        return page