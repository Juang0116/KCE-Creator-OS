from src.brand_brain import BrandBrainV0
from src.radar import RadarV0


def create_signal(
    title: str,
    keywords: list[str],
    topics: list[str],
):
    raw_signal = {
        "title": title,
        "summary": "Señal de prueba para Brand Brain.",
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
    }


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