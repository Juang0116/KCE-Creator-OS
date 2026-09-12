from src.brand_brain.technology import (
    TechnologyClassifierV1_2,
)


def classify(
    title="",
    summary="",
    keywords=None,
    topics=None,
):
    return TechnologyClassifierV1_2().classify(
        title=title,
        summary=summary,
        keywords=keywords or [],
        topics=topics or [],
    )


def test_gpu_is_core_hardware():
    evidence = classify(
        title="NVIDIA launches a new GPU architecture",
        summary="The new GPU improves compute performance.",
    )

    assert evidence.technology_domain == "hardware"
    assert evidence.technology_centrality == "core"
    assert "gpu" in evidence.specific_evidence
    assert "hardware" in evidence.matched_domains


def test_pytorch_is_core_developer_technology():
    evidence = classify(
        title="PyTorch introduces a new training optimization",
        summary="Developers can train machine learning models faster.",
    )

    assert evidence.technology_domain == "developer_tools"
    assert evidence.technology_centrality == "core"
    assert "pytorch" in evidence.specific_evidence


def test_cuda_is_core_developer_technology():
    evidence = classify(
        title="CUDA changes how developers use GPUs",
        summary="The new tooling improves GPU programming.",
    )

    assert evidence.technology_domain == "developer_tools"
    assert evidence.technology_centrality == "core"
    assert "cuda" in evidence.specific_evidence


def test_sora_is_core_ai():
    evidence = classify(
        title="Sora changes AI video generation",
        summary="The model generates video from text prompts.",
    )

    assert evidence.technology_domain == "ai"
    assert evidence.technology_centrality == "core"
    assert "sora" in evidence.specific_evidence


def test_rag_is_core_ai():
    evidence = classify(
        title="RAG improves how AI answers questions",
        summary="Retrieval augmented generation gives models external context.",
    )

    assert evidence.technology_domain == "ai"
    assert evidence.technology_centrality == "core"
    assert "rag" in evidence.specific_evidence


def test_dota_ai_is_core_ai():
    evidence = classify(
        title="Dota AI learns new strategies",
        summary="An AI system is trained to play the game.",
    )

    assert evidence.technology_domain == "ai"
    assert evidence.technology_centrality == "core"
    assert "dota ai" in evidence.specific_evidence


def test_robotics_is_core_robotics():
    evidence = classify(
        title="Humanoid robots learn new physical tasks",
        summary="Robotics researchers demonstrate autonomous movement.",
    )

    assert evidence.technology_domain == "robotics"
    assert evidence.technology_centrality == "core"


def test_quantum_computing_is_core_science_technology():
    evidence = classify(
        title="Quantum computing experiment achieves new result",
        summary="Researchers use a quantum computer for the experiment.",
    )

    assert evidence.technology_domain == "science_technology"
    assert evidence.technology_centrality == "core"


def test_fishing_with_chatgpt_is_not_core_technology():
    evidence = classify(
        title="A fisherman uses ChatGPT to plan a fishing trip",
        summary="He asks ChatGPT for advice about local fishing conditions.",
    )

    assert evidence.technology_centrality == "incidental"
    assert "chatgpt" in evidence.generic_evidence


def test_generic_openai_company_mention_is_not_automatically_core():
    evidence = classify(
        title="OpenAI expands its presence in Japan",
        summary="The company announces a new local initiative.",
    )

    assert evidence.technology_centrality in {
        "supporting",
        "incidental",
    }


def test_generic_ai_without_specific_context_is_incidental():
    evidence = classify(
        title="AI is changing the future",
        summary="Experts discuss the growing importance of artificial intelligence.",
    )

    assert evidence.technology_centrality == "incidental"
    assert evidence.technology_domain == "ai"


def test_football_signal_has_no_technology():
    evidence = classify(
        title="Real Madrid signs a new football player",
        summary="The club announces a new transfer.",
        keywords=["Real Madrid", "football", "transfer"],
        topics=["sports", "football"],
    )

    assert evidence.technology_domain == "none"
    assert evidence.technology_centrality == "none"
    assert evidence.matched_domains == []
    assert evidence.specific_evidence == []


def test_metadata_can_provide_supporting_evidence():
    evidence = classify(
        title="A new product launches today",
        summary="The company announces its latest offering.",
        keywords=["GPU", "hardware"],
        topics=["hardware"],
    )

    assert evidence.technology_domain == "hardware"
    assert evidence.technology_centrality == "supporting"


def test_multiple_domains_in_content_are_core():
    evidence = classify(
        title="New GPU software platform for AI developers",
        summary="The platform combines hardware acceleration with developer tools.",
    )

    assert evidence.technology_centrality == "core"
    assert evidence.technology_domain in {
        "hardware",
        "developer_tools",
        "ai",
        "software",
    }


def test_to_dict_is_serializable():
    evidence = classify(
        title="CUDA improves GPU computing",
    )

    data = evidence.to_dict()

    assert data["technology_domain"] == "developer_tools"
    assert data["technology_centrality"] == "core"
    assert isinstance(data["matched_terms"], list)
    assert isinstance(data["matched_domains"], list)
    assert isinstance(data["specific_evidence"], list)
    assert isinstance(data["generic_evidence"], list)