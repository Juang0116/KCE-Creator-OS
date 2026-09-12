from __future__ import annotations

from datetime import datetime, timezone

from .models import ResearchBrief
from .provider import ResearchProvider


class ResearchExecutionEngineV1:
    """
    Executes a prepared ResearchBrief through a ResearchProvider.

    V1 keeps the execution boundary deterministic and provider-agnostic.
    External research technologies are injected through the provider
    contract instead of being coupled to the Research domain.
    """

    VERSION = "1.0.0"

    def execute(
        self,
        brief: ResearchBrief,
        provider: ResearchProvider,
    ) -> ResearchBrief:
        if brief is None:
            raise ValueError(
                "ResearchBrief must not be None."
            )

        if provider is None:
            raise ValueError(
                "ResearchProvider must not be None."
            )

        result = provider.research(brief)

        if result is None:
            raise ValueError(
                "ResearchProvider must return a result."
            )

        brief.sources = list(result.sources)
        brief.findings = list(result.findings)
        brief.research_gaps = list(
            result.research_gaps
        )

        brief.processing.status = "completed"
        brief.processing.confidence = (
            self._calculate_confidence(brief)
        )
        brief.processing.processed_at = (
            datetime.now(timezone.utc).isoformat()
        )

        brief.research_version = self.VERSION

        return brief

    @staticmethod
    def _calculate_confidence(
        brief: ResearchBrief,
    ) -> float:
        """
        Calculate aggregate research confidence.

        No findings means no evidentiary confidence.
        Otherwise confidence is the average confidence
        of the collected findings.
        """

        if not brief.findings:
            return 0.0

        total = sum(
            max(
                min(
                    finding.confidence,
                    1.0,
                ),
                0.0,
            )
            for finding in brief.findings
        )

        return min(
            max(
                total / len(brief.findings),
                0.0,
            ),
            1.0,
        )