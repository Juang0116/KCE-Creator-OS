from typing import Any

from src.orchestration import DiscoveryPackage


class NotionDiscoveryMapper:
    """
    Maps a DiscoveryPackage into Notion database properties.

    This class does not communicate with Notion.
    """

    def map(
        self,
        package: DiscoveryPackage,
    ) -> dict[str, Any]:

        discovery = package.discovery
        idea = discovery.idea
        opportunity = discovery.opportunity
        approval = package.approval

        if idea is None:
            raise ValueError(
                "Cannot map a DiscoveryPackage "
                "without a ContentIdea."
            )

        if approval is None:
            raise ValueError(
                "Cannot map a DiscoveryPackage "
                "without a DiscoveryApproval."
            )

        return {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": (
                                idea.concept
                            )
                        }
                    }
                ]
            },
            "Status": {
                "select": {
                    "name": "Pendiente de Revisión"
                }
            },
            "Channel": {
                "rich_text": [
                    {
                        "text": {
                            "content": idea.channel
                        }
                    }
                ]
            },
            "Platform": {
                "select": {
                    "name": idea.platform
                }
            },
            "Topic": {
                "rich_text": [
                    {
                        "text": {
                            "content": (
                                opportunity.analysis.why_now
                            )
                        }
                    }
                ]
            },
            "Priority": {
                "select": {
                    "name": self._map_priority(
                        opportunity.scoring.total_score
                    )
                }
            },
            "Discovery ID": {
                "rich_text": [
                    {
                        "text": {
                            "content": (
                                discovery.discovery_id
                            )
                        }
                    }
                ]
            },
            "Signal ID": {
                "rich_text": [
                    {
                        "text": {
                            "content": (
                                discovery.signal.signal_id
                            )
                        }
                    }
                ]
            },
            "Opportunity ID": {
                "rich_text": [
                    {
                        "text": {
                            "content": (
                                opportunity.opportunity_id
                            )
                        }
                    }
                ]
            },
            "Idea ID": {
                "rich_text": [
                    {
                        "text": {
                            "content": idea.idea_id
                        }
                    }
                ]
            },
            "Approval ID": {
                "rich_text": [
                    {
                        "text": {
                            "content": (
                                approval.approval_id
                            )
                        }
                    }
                ]
            },
        }

    @staticmethod
    def _map_priority(
        score: float,
    ) -> str:

        if score >= 80:
            return "Critical"

        if score >= 60:
            return "High"

        if score >= 40:
            return "Medium"

        return "Low"