from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .models import ResearchBrief, ResearchFinding, ResearchSource


@dataclass(frozen=True)
class ResearchProviderResult:
    """
    Normalized output produced by a research provider.

    Providers may use completely different external
    technologies, but Research receives a stable internal
    representation.
    """

    sources: list[ResearchSource]
    findings: list[ResearchFinding]
    research_gaps: list[str]


class ResearchProvider(Protocol):
    """
    Contract for executable research providers.

    The provider is responsible for gathering and normalizing
    research evidence. It does not own Research domain state.
    """

    def research(
        self,
        brief: ResearchBrief,
    ) -> ResearchProviderResult:
        """
        Execute research for a prepared ResearchBrief.
        """
        ...