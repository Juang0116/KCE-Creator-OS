from src.brand_brain import BrandBrainV0
from src.radar import RadarV0


def create_signal(
    title: str,
    keywords: list[str],
    topics: list[str],
    summary: str = "Señal de prueba para Brand Brain.",
):
    raw_signal = {
        "title": title,
        "summary": summary,
        "source_type": "news",
        "platform": "TestSource",
        "keywords": keywords,
        "topics": topics,
        "language": "es",
        "niches": ["technology"],
        "relevance_reason": "Señal creada para pruebas.",
    }

    return RadarV0().collect([raw_signal])[0]


def create_futuro_tech_brand():
    return {
        "brand_id": "futuro_tech",
        "identity": {
            "name": "Futuro Tech",
            "value_proposition": (
                "Explicar tecnología de forma clara y accesible."
            ),
        },
        "content": {
            "pillars": [
                "technology",
                "AI",
                "hardware",
                "PC",
            ],
            "topics": [
                "GPU",
                "AI",
                "creators",
            ],
        },
        "audience": {
            "interests": [
                "technology",
                "AI",
                "software",
                "robotics",
            ],
            "problems": [
                "entender tecnología compleja",
            ],
            "desires": [
                "aprender sobre tecnología",
            ],
        },
        "channels": {
            "primary_platforms": ["YouTube"],
        },
    }


# ---------------------------------------------------------------------------
# V0 REGRESSION TESTS
# ---------------------------------------------------------------------------


def test_relevant_signal():
    signal = create_signal(
        title="Nueva GPU para inteligencia artificial",
        keywords=["GPU", "AI"],
        topics=["technology", "AI"],
    )

    brand = create_futuro_tech_brand()

    evaluation = BrandBrainV0().evaluate(signal, brand)

    assert evaluation.relevant is True
    assert evaluation.relevance_score > 0
    assert "technology" in evaluation.matched_pillars
    assert "AI" in evaluation.matched_pillars
    assert "GPU" in evaluation.matched_topics


def test_irrelevant_signal():
    signal = create_signal(
        title="Nuevo fichaje del Real Madrid",
        keywords=["Real Madrid", "football"],
        topics=["sports", "football"],
    )

    brand = create_futuro_tech_brand()

    evaluation = BrandBrainV0().evaluate(signal, brand)

    assert evaluation.relevant is False
    assert evaluation.relevance_score == 0
    assert evaluation.matched_pillars == []
    assert evaluation.matched_topics == []


def test_partially_relevant_signal():
    signal = create_signal(
        title="Nuevo monitor para gaming",
        keywords=["monitor", "gaming"],
        topics=["technology"],
    )

    brand = create_futuro_tech_brand()

    evaluation = BrandBrainV0().evaluate(signal, brand)

    assert evaluation.relevant is True
    assert evaluation.relevance_score > 0
    assert "technology" in evaluation.matched_pillars


# ---------------------------------------------------------------------------
# V1 CONTRACT TESTS
# ---------------------------------------------------------------------------


def test_brand_evaluation_v1_exposes_dimensions():
    signal = create_signal(
        title="AI coding agents transform software development",
        keywords=["AI", "software", "coding"],
        topics=["AI", "software"],
        summary=(
            "AI coding agents are transforming software development "
            "and helping people understand new technology."
        ),
    )

    brand = create_futuro_tech_brand()

    evaluation = BrandBrainV0().evaluate(signal, brand)

    assert hasattr(evaluation, "dimensions")
    assert "pillar_fit" in evaluation.dimensions
    assert "topic_fit" in evaluation.dimensions
    assert "audience_fit" in evaluation.dimensions
    assert "brand_promise_fit" in evaluation.dimensions
    assert "context_fit" in evaluation.dimensions

    assert 0 <= evaluation.relevance_score <= 100


def test_brand_evaluation_v1_dimensions_are_normalized():
    signal = create_signal(
        title="AI software platform",
        keywords=["AI", "software"],
        topics=["AI", "software"],
    )

    brand = create_futuro_tech_brand()

    evaluation = BrandBrainV0().evaluate(signal, brand)

    for dimension_name, dimension_score in evaluation.dimensions.items():
        assert dimension_name in {
            "pillar_fit",
            "topic_fit",
            "audience_fit",
            "brand_promise_fit",
            "context_fit",
        }
        assert 0 <= dimension_score <= 10


def test_brand_evaluation_v1_exposes_relevance_level():
    signal = create_signal(
        title="AI coding agents transform software development",
        keywords=["AI", "software", "coding"],
        topics=["AI", "software"],
    )

    brand = create_futuro_tech_brand()

    evaluation = BrandBrainV0().evaluate(signal, brand)

    assert hasattr(evaluation, "relevance_level")
    assert evaluation.relevance_level in {
        "highly_relevant",
        "relevant",
        "borderline",
        "irrelevant",
    }


def test_brand_evaluation_v1_exposes_positive_and_negative_reasons():
    signal = create_signal(
        title="AI coding agents transform software development",
        keywords=["AI", "software", "coding"],
        topics=["AI", "software"],
    )

    brand = create_futuro_tech_brand()

    evaluation = BrandBrainV0().evaluate(signal, brand)

    assert hasattr(evaluation, "positive_reasons")
    assert hasattr(evaluation, "negative_reasons")

    assert isinstance(evaluation.positive_reasons, list)
    assert isinstance(evaluation.negative_reasons, list)


def test_brand_evaluation_v1_preserves_rule_flags():
    signal = create_signal(
        title="Team update",
        keywords=["AI", "software"],
        topics=["AI"],
    )

    brand = create_futuro_tech_brand()

    evaluation = BrandBrainV0().evaluate(signal, brand)

    assert hasattr(evaluation, "rule_flags")
    assert isinstance(evaluation.rule_flags, list)


# ---------------------------------------------------------------------------
# V1 BEHAVIOR TESTS
# ---------------------------------------------------------------------------


def test_pillar_fit_is_higher_for_core_pillar():
    ai_signal = create_signal(
        title="New AI system",
        keywords=["AI"],
        topics=["AI"],
    )

    hardware_signal = create_signal(
        title="New hardware device",
        keywords=["hardware"],
        topics=["hardware"],
    )

    brand = create_futuro_tech_brand()

    ai_evaluation = BrandBrainV0().evaluate(ai_signal, brand)
    hardware_evaluation = BrandBrainV0().evaluate(
        hardware_signal,
        brand,
    )

    assert (
        ai_evaluation.dimensions["pillar_fit"]
        >= hardware_evaluation.dimensions["pillar_fit"]
    )


def test_topic_fit_recognizes_specific_brand_topics():
    signal = create_signal(
        title="New GPU for creators",
        keywords=["GPU", "creators"],
        topics=["GPU", "creators"],
    )

    brand = create_futuro_tech_brand()

    evaluation = BrandBrainV0().evaluate(signal, brand)

    assert "GPU" in evaluation.matched_topics
    assert evaluation.dimensions["topic_fit"] > 0


def test_audience_fit_uses_brand_audience():
    signal = create_signal(
        title="AI software development tools",
        keywords=["AI", "software"],
        topics=["AI", "software"],
    )

    brand = create_futuro_tech_brand()

    evaluation = BrandBrainV0().evaluate(signal, brand)

    assert evaluation.dimensions["audience_fit"] > 0


def test_brand_promise_fit_uses_value_proposition():
    signal = create_signal(
        title="How AI coding agents work",
        keywords=["AI", "coding", "software"],
        topics=["AI", "software"],
        summary=(
            "An accessible explanation of how AI coding agents work "
            "and why they matter."
        ),
    )

    brand = create_futuro_tech_brand()

    evaluation = BrandBrainV0().evaluate(signal, brand)

    assert evaluation.dimensions["brand_promise_fit"] > 0


def test_context_fit_uses_signal_context():
    strong_context_signal = create_signal(
        title="NVIDIA acquires Hugging Face to expand AI infrastructure",
        keywords=["AI", "NVIDIA", "Hugging Face"],
        topics=["AI"],
        summary=(
            "NVIDIA has agreed to acquire Hugging Face, bringing together "
            "AI infrastructure, developers, and open-source technology."
        ),
    )

    weak_context_signal = create_signal(
        title="Team update",
        keywords=["AI"],
        topics=["AI"],
        summary="A short generic company update.",
    )

    brand = create_futuro_tech_brand()

    strong_evaluation = BrandBrainV0().evaluate(
        strong_context_signal,
        brand,
    )

    weak_evaluation = BrandBrainV0().evaluate(
        weak_context_signal,
        brand,
    )

    assert (
        strong_evaluation.dimensions["context_fit"]
        >= weak_evaluation.dimensions["context_fit"]
    )


def test_generic_team_update_does_not_gain_relevance_only_from_keywords():
    signal = create_signal(
        title="Team update",
        keywords=["AI", "software", "robots", "OpenAI"],
        topics=["AI", "software"],
        summary="A generic team update.",
    )

    brand = create_futuro_tech_brand()

    evaluation = BrandBrainV0().evaluate(signal, brand)

    assert evaluation.relevance_level != "highly_relevant"


def test_nvidia_hugging_face_is_relevant():
    signal = create_signal(
        title="NVIDIA acquires Hugging Face",
        keywords=["AI", "developers", "NVIDIA", "Hugging Face"],
        topics=["AI"],
        summary=(
            "NVIDIA has agreed to acquire Hugging Face, strengthening "
            "AI infrastructure and expanding access to AI for developers."
        ),
    )

    brand = create_futuro_tech_brand()

    evaluation = BrandBrainV0().evaluate(signal, brand)

    assert evaluation.relevant is True
    assert evaluation.relevance_score >= 65


def test_scientific_computing_agentic_ai_is_relevant():
    signal = create_signal(
        title="Scientific computing in the age of agentic AI",
        keywords=[
            "AI",
            "agentic AI",
            "agentic",
            "agents",
            "software",
            "coding",
        ],
        topics=[
            "AI",
            "agentic AI",
            "software",
        ],
        summary=(
            "Scientists use AI coding agents to modernize scientific "
            "computing, accelerating software development and discovery."
        ),
    )

    brand = create_futuro_tech_brand()

    evaluation = BrandBrainV0().evaluate(signal, brand)

    assert evaluation.relevant is True
    assert evaluation.relevance_score >= 65


def test_irrelevant_sports_signal_remains_irrelevant():
    signal = create_signal(
        title="Real Madrid signs new football player",
        keywords=["Real Madrid", "football", "transfer"],
        topics=["sports", "football"],
    )

    brand = create_futuro_tech_brand()

    evaluation = BrandBrainV0().evaluate(signal, brand)

    assert evaluation.relevant is False
    assert evaluation.relevance_level == "irrelevant"


# ---------------------------------------------------------------------------
# V1.1 GENERIC AI EVIDENCE TESTS
# ---------------------------------------------------------------------------


def test_generic_ai_only_signal_does_not_become_relevant_automatically():
    signal = create_signal(
        title="AI policy",
        keywords=["AI"],
        topics=["AI"],
        summary="A general discussion about AI policy.",
    )

    brand = create_futuro_tech_brand()

    evaluation = BrandBrainV0().evaluate(signal, brand)

    assert evaluation.relevant is False
    assert evaluation.relevance_level == "borderline"
    assert "no_specific_topic_evidence" in evaluation.rule_flags


def test_chatgpt_financial_services_is_not_relevant_from_ai_alone():
    signal = create_signal(
        title="Introducing ChatGPT for Financial Services",
        keywords=["AI", "ChatGPT"],
        topics=["AI"],
        summary=(
            "A financial services application using GPT technology."
        ),
    )

    brand = create_futuro_tech_brand()

    evaluation = BrandBrainV0().evaluate(signal, brand)

    assert evaluation.relevant is False
    assert evaluation.relevance_level == "borderline"


def test_specific_ai_topic_overrides_generic_ai_filter():
    signal = create_signal(
        title="AI coding agents transform software development",
        keywords=["AI", "coding", "software"],
        topics=["AI", "software"],
        summary=(
            "AI coding agents are changing software development."
        ),
    )

    brand = create_futuro_tech_brand()

    evaluation = BrandBrainV0().evaluate(signal, brand)

    assert evaluation.relevant is True
    assert evaluation.relevance_score >= 65
    assert "no_specific_topic_evidence" not in evaluation.rule_flags


def test_strong_generic_ai_context_can_establish_relevance():
    signal = create_signal(
        title="New AI system launches",
        keywords=["AI"],
        topics=["AI"],
        summary=(
            "A new AI system launches after research and development "
            "for developers and technology infrastructure."
        ),
    )

    brand = create_futuro_tech_brand()

    evaluation = BrandBrainV0().evaluate(signal, brand)

    assert evaluation.relevant is True
    assert evaluation.dimensions["context_fit"] >= 8