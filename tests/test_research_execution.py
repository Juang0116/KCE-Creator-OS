from src.research import (
    ResearchEngineV0,
    ResearchExecutionEngineV1,
    ResearchFinding,
    ResearchProviderResult,
    ResearchSource,
)

from test_research_engine import (
    create_brand,
    create_content_idea,
)


class FakeResearchProvider:
    def research(self, brief):
        return ResearchProviderResult(
            sources=[
                ResearchSource(
                    source_id="source_001",
                    title="Test source",
                    url="https://example.com/source",
                    publisher="Test Publisher",
                    source_type="reference",
                    reliability=0.9,
                )
            ],
            findings=[
                ResearchFinding(
                    claim="La GPU tiene relevancia para creadores.",
                    evidence="Evidence collected by test provider.",
                    source_id="source_001",
                    confidence=0.9,
                )
            ],
            research_gaps=[
                "Additional market data is required.",
            ],
        )


def create_research():
    idea = create_content_idea()
    brand = create_brand()

    return ResearchEngineV0().generate(
        idea,
        brand,
    )


def test_research_execution_completes_brief():
    brief = create_research()

    provider = FakeResearchProvider()

    result = ResearchExecutionEngineV1().execute(
        brief=brief,
        provider=provider,
    )

    assert result is brief
    assert result.processing.status == "completed"
    assert result.processing.processed_at is not None


def test_research_execution_populates_sources():
    brief = create_research()

    result = ResearchExecutionEngineV1().execute(
        brief=brief,
        provider=FakeResearchProvider(),
    )

    assert len(result.sources) == 1
    assert result.sources[0].source_id == "source_001"


def test_research_execution_populates_findings():
    brief = create_research()

    result = ResearchExecutionEngineV1().execute(
        brief=brief,
        provider=FakeResearchProvider(),
    )

    assert len(result.findings) == 1
    assert (
        result.findings[0].claim
        == "La GPU tiene relevancia para creadores."
    )


def test_research_execution_populates_research_gaps():
    brief = create_research()

    result = ResearchExecutionEngineV1().execute(
        brief=brief,
        provider=FakeResearchProvider(),
    )

    assert result.research_gaps == [
        "Additional market data is required.",
    ]


def test_research_execution_calculates_confidence():
    brief = create_research()

    result = ResearchExecutionEngineV1().execute(
        brief=brief,
        provider=FakeResearchProvider(),
    )

    assert result.processing.confidence == 0.9


def test_research_execution_rejects_missing_brief():
    provider = FakeResearchProvider()

    try:
        ResearchExecutionEngineV1().execute(
            brief=None,
            provider=provider,
        )
    except ValueError as exc:
        assert str(exc) == (
            "ResearchBrief must not be None."
        )
    else:
        raise AssertionError(
            "Expected ValueError."
        )


def test_research_execution_rejects_missing_provider():
    brief = create_research()

    try:
        ResearchExecutionEngineV1().execute(
            brief=brief,
            provider=None,
        )
    except ValueError as exc:
        assert str(exc) == (
            "ResearchProvider must not be None."
        )
    else:
        raise AssertionError(
            "Expected ValueError."
        )


def test_research_execution_rejects_provider_without_result():
    class EmptyProvider:
        def research(self, brief):
            return None

    brief = create_research()

    try:
        ResearchExecutionEngineV1().execute(
            brief=brief,
            provider=EmptyProvider(),
        )
    except ValueError as exc:
        assert str(exc) == (
            "ResearchProvider must return a result."
        )
    else:
        raise AssertionError(
            "Expected ValueError."
        )