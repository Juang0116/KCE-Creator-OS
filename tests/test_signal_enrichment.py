from src.enrichment import SignalEnrichmentEngineV0


def test_enrichment_detects_keywords_from_title_and_summary():
    engine = SignalEnrichmentEngineV0()

    result = engine.enrich(
        title="NVIDIA launches new AI chips",
        summary=(
            "The company announced new GPU technology "
            "for artificial intelligence workloads."
        ),
    )

    assert "NVIDIA" in result.keywords
    assert "AI" in result.keywords
    assert "GPU" in result.keywords

    assert "AI" in result.topics
    assert "chips" in result.topics


def test_enrichment_preserves_existing_keywords_and_topics():
    engine = SignalEnrichmentEngineV0()

    result = engine.enrich(
        title="New AI platform",
        summary="A software platform for developers.",
        existing_keywords=["Product"],
        existing_topics=["Product"],
    )

    assert "Product" in result.keywords
    assert "Product" in result.topics

    assert "AI" in result.keywords
    assert "software" in result.keywords


def test_enrichment_deduplicates_terms():
    engine = SignalEnrichmentEngineV0()

    result = engine.enrich(
        title="AI and artificial intelligence",
        summary="AI technology for developers.",
        existing_keywords=["AI", "AI"],
        existing_topics=["AI", "AI"],
    )

    assert result.keywords.count("AI") == 1
    assert result.topics.count("AI") == 1


def test_enrichment_is_case_insensitive():
    engine = SignalEnrichmentEngineV0()

    result = engine.enrich(
        title="OPENAI announces new AI tools",
        summary="Developers can use the new API.",
    )

    assert "OpenAI" in result.keywords
    assert "AI" in result.keywords
    assert "API" in result.keywords


def test_enrichment_does_not_match_partial_words():
    engine = SignalEnrichmentEngineV0()

    result = engine.enrich(
        title="Artificial intelligent systems",
        summary="A company discusses gaming.",
    )

    assert "AI" not in result.keywords
    assert "artificial intelligence" not in result.keywords


def test_enrichment_returns_processing_metadata():
    engine = SignalEnrichmentEngineV0()

    result = engine.enrich(
        title="AI research",
        summary="New research.",
    )

    assert result.processing["status"] == "enriched"
    assert result.processing["method"] == "deterministic_taxonomy"
    assert result.processing["taxonomy_version"] == "0.2.0"


def test_enrichment_derives_ai_from_codex():
    engine = SignalEnrichmentEngineV0()

    result = engine.enrich(
        title="How researchers use Codex",
        summary="Codex helps researchers write and analyze code.",
    )

    assert "Codex" in result.keywords
    assert "AI" in result.topics
    assert "AI coding" in result.topics
    assert "developer tools" in result.topics
    assert "software" in result.topics


def test_enrichment_derives_ai_from_chatgpt():
    engine = SignalEnrichmentEngineV0()

    result = engine.enrich(
        title="Introducing ChatGPT for Financial Services",
        summary="Organizations can use ChatGPT for new workflows.",
    )

    assert "ChatGPT" in result.keywords
    assert "AI" in result.topics
    assert "generative AI" in result.topics
    assert "AI applications" in result.topics


def test_enrichment_derives_ai_from_gpt():
    engine = SignalEnrichmentEngineV0()

    result = engine.enrich(
        title="A new GPT model for developers",
        summary="The model improves software development.",
    )

    assert "GPT" in result.keywords
    assert "AI" in result.topics
    assert "generative AI" in result.topics


def test_enrichment_derives_multiple_concepts_from_ai_agents():
    engine = SignalEnrichmentEngineV0()

    result = engine.enrich(
        title="New AI agents for software development",
        summary="Agentic AI can automate developer workflows.",
    )

    assert "AI agents" in result.keywords
    assert "agentic AI" in result.keywords

    assert "AI" in result.topics
    assert "AI agents" in result.topics
    assert "software" in result.topics


def test_enrichment_derives_hardware_concepts_from_nvidia():
    engine = SignalEnrichmentEngineV0()

    result = engine.enrich(
        title="NVIDIA announces a new platform",
        summary="The company develops hardware and GPUs for AI.",
    )

    assert "NVIDIA" in result.keywords
    assert "GPUs" in result.keywords

    assert "AI" in result.topics
    assert "hardware" in result.topics
    assert "chips" in result.topics


def test_enrichment_recovers_codex_signal_without_existing_categories():
    engine = SignalEnrichmentEngineV0()

    result = engine.enrich(
        title="1Password increases engineering productivity with Codex",
        summary="The company uses Codex to improve software engineering.",
        existing_keywords=[],
        existing_topics=[],
    )

    assert "Codex" in result.keywords
    assert "AI" in result.topics
    assert "AI coding" in result.topics
    assert "software" in result.topics


def test_enrichment_preserves_generic_existing_category_while_deriving_ai():
    engine = SignalEnrichmentEngineV0()

    result = engine.enrich(
        title="Introducing ChatGPT for Financial Services",
        summary="A new product uses generative AI.",
        existing_keywords=["Product"],
        existing_topics=["Product"],
    )

    assert "Product" in result.keywords
    assert "Product" in result.topics

    assert "ChatGPT" in result.keywords
    assert "AI" in result.topics
    assert "generative AI" in result.topics