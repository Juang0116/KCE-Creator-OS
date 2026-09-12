from __future__ import annotations

import re

from .models import SignalEnrichmentResult


class SignalEnrichmentEngineV0:
    """
    Signal Enrichment V1.

    Responsabilidad:
    - analizar title + summary + categorías existentes;
    - detectar términos literales mediante una taxonomía determinista;
    - derivar conceptos canónicos relacionados;
    - producir keywords y topics más útiles para Brand Brain;
    - conservar las categorías originales.

    No:
    - consulta APIs externas;
    - utiliza LLMs;
    - evalúa relevancia de marca;
    - calcula oportunidades;
    - modifica RadarSignal directamente.
    """

    DEFAULT_TAXONOMY = {
        "AI": {
            "keywords": [
                "AI",
                "artificial intelligence",
                "applied AI",
                "generative AI",
                "genai",
                "machine learning",
                "deep learning",
                "large language model",
                "large language models",
                "LLM",
                "LLMs",
            ],
            "topics": [
                "AI",
                "artificial intelligence",
                "machine learning",
                "generative AI",
            ],
        },
        "AI coding": {
            "keywords": [
                "Codex",
                "AI coding",
                "AI code",
                "AI programming",
                "coding agent",
                "coding agents",
            ],
            "topics": [
                "AI coding",
                "developer tools",
            ],
        },
        "AI applications": {
            "keywords": [
                "ChatGPT",
                "GPT",
                "GPT-5",
                "GPT-6",
                "Claude",
                "Gemini",
                "AI application",
                "AI applications",
                "AI-native",
                "AI native",
            ],
            "topics": [
                "generative AI",
                "AI applications",
            ],
        },
        "agents": {
            "keywords": [
                "AI agent",
                "AI agents",
                "agentic AI",
                "agentic",
                "agents",
                "agent",
            ],
            "topics": [
                "AI agents",
                "agentic AI",
            ],
        },
        "software": {
            "keywords": [
                "software",
                "programming",
                "developer",
                "developers",
                "coding",
                "code",
                "API",
                "APIs",
                "application",
                "applications",
                "platform",
                "platforms",
            ],
            "topics": [
                "software",
                "programming",
                "developer tools",
            ],
        },
        "robotics": {
            "keywords": [
                "robot",
                "robots",
                "robotics",
                "physical AI",
                "humanoid",
                "humanoids",
            ],
            "topics": [
                "robotics",
                "physical AI",
            ],
        },
        "chips": {
            "keywords": [
                "GPU",
                "GPUs",
                "CPU",
                "CPUs",
                "chip",
                "chips",
                "semiconductor",
                "semiconductors",
                "NVIDIA",
                "AMD",
                "Intel",
                "Qualcomm",
                "TSMC",
            ],
            "topics": [
                "chips",
                "semiconductors",
                "hardware",
            ],
        },
        "hardware": {
            "keywords": [
                "hardware",
                "computer hardware",
                "PC hardware",
                "processor",
                "processors",
                "graphics card",
                "graphics cards",
                "GPU",
                "GPUs",
                "CPU",
                "CPUs",
            ],
            "topics": [
                "hardware",
                "PC hardware",
            ],
        },
        "cloud": {
            "keywords": [
                "cloud",
                "cloud computing",
                "cloud infrastructure",
                "AWS",
                "Azure",
                "Google Cloud",
            ],
            "topics": [
                "cloud computing",
                "cloud infrastructure",
            ],
        },
        "cybersecurity": {
            "keywords": [
                "cybersecurity",
                "cyber security",
                "security",
                "threat",
                "threats",
                "malware",
                "ransomware",
                "zero trust",
                "cyber attack",
                "cyber attacks",
            ],
            "topics": [
                "cybersecurity",
            ],
        },
        "automation": {
            "keywords": [
                "automation",
                "automated",
                "workflow automation",
                "workflow",
                "workflows",
            ],
            "topics": [
                "automation",
                "workflow automation",
            ],
        },
        "computer_vision": {
            "keywords": [
                "computer vision",
                "image recognition",
                "visual recognition",
                "object detection",
            ],
            "topics": [
                "computer vision",
            ],
        },
        "companies": {
            "keywords": [
                "OpenAI",
                "Google",
                "Google DeepMind",
                "Microsoft",
                "Apple",
                "Meta",
                "NVIDIA",
                "Hugging Face",
                "Anthropic",
                "Amazon",
            ],
            "topics": [
                "AI companies",
                "technology companies",
            ],
        },
        "sports_technology": {
            "keywords": [
                "sports",
                "broadcast",
                "broadcasting",
                "streaming",
                "sports technology",
            ],
            "topics": [
                "sports technology",
                "broadcasting",
                "streaming",
            ],
        },
    }

    # Conceptos derivados.
    #
    # La clave es el término que actúa como evidencia.
    # Los valores son conceptos canónicos que deben agregarse
    # cuando aparece esa evidencia.
    DERIVED_CONCEPTS = {
        "Codex": {
            "keywords": ["Codex"],
            "topics": ["AI", "AI coding", "developer tools", "software"],
        },
        "ChatGPT": {
            "keywords": ["ChatGPT"],
            "topics": ["AI", "generative AI", "AI applications"],
        },
        "GPT": {
            "keywords": ["GPT"],
            "topics": ["AI", "generative AI"],
        },
        "GPT-5": {
            "keywords": ["GPT-5"],
            "topics": ["AI", "generative AI"],
        },
        "GPT-6": {
            "keywords": ["GPT-6"],
            "topics": ["AI", "generative AI"],
        },
        "Claude": {
            "keywords": ["Claude"],
            "topics": ["AI", "generative AI"],
        },
        "Gemini": {
            "keywords": ["Gemini"],
            "topics": ["AI", "generative AI"],
        },
        "AI agents": {
            "keywords": ["AI agents"],
            "topics": ["AI", "AI agents", "software"],
        },
        "agentic AI": {
            "keywords": ["agentic AI"],
            "topics": ["AI", "AI agents", "software"],
        },
        "agentic": {
            "keywords": ["agentic"],
            "topics": ["AI", "AI agents"],
        },
        "NVIDIA": {
            "keywords": ["NVIDIA"],
            "topics": ["AI", "hardware", "chips"],
        },
        "GPU": {
            "keywords": ["GPU"],
            "topics": ["hardware", "chips"],
        },
        "GPUs": {
            "keywords": ["GPUs"],
            "topics": ["hardware", "chips"],
        },
        "machine learning": {
            "keywords": ["machine learning"],
            "topics": ["AI", "machine learning"],
        },
        "deep learning": {
            "keywords": ["deep learning"],
            "topics": ["AI", "machine learning"],
        },
        "physical AI": {
            "keywords": ["physical AI"],
            "topics": ["AI", "robotics"],
        },
        "computer vision": {
            "keywords": ["computer vision"],
            "topics": ["AI", "computer vision"],
        },
        "AI-native": {
            "keywords": ["AI-native"],
            "topics": ["AI", "AI applications"],
        },
        "AI native": {
            "keywords": ["AI native"],
            "topics": ["AI", "AI applications"],
        },
    }

    def __init__(self, taxonomy: dict | None = None):
        self.taxonomy = taxonomy or self.DEFAULT_TAXONOMY

    def enrich(
        self,
        title: str,
        summary: str,
        existing_keywords: list[str] | None = None,
        existing_topics: list[str] | None = None,
    ) -> SignalEnrichmentResult:
        """
        Enriquece una señal sin modificar la señal original.

        La detección se realiza sobre title + summary.

        Las categorías existentes se conservan y se combinan
        con los conceptos detectados y derivados.
        """

        title = title or ""
        summary = summary or ""

        text = self._normalize_text(
            f"{title} {summary}"
        )

        keywords = self._clean_terms(
            existing_keywords or []
        )

        topics = self._clean_terms(
            existing_topics or []
        )

        matched_terms = []

        # 1. Detección directa de la taxonomía.
        for category in self.taxonomy.values():
            for keyword in category.get("keywords", []):
                if self._contains_term(text, keyword):
                    keywords.append(keyword)
                    matched_terms.append(keyword)

            for topic in category.get("topics", []):
                if self._contains_term(text, topic):
                    topics.append(topic)

        # 2. Derivación conceptual.
        #
        # Esta capa no reemplaza la detección directa.
        # Añade conocimiento canónico a partir de términos
        # que funcionan como evidencia.
        for evidence_term, concepts in self.DERIVED_CONCEPTS.items():
            if not self._contains_term(text, evidence_term):
                continue

            for keyword in concepts.get("keywords", []):
                keywords.append(keyword)

            for topic in concepts.get("topics", []):
                topics.append(topic)

            matched_terms.append(evidence_term)

        keywords = self._unique_preserving_order(keywords)
        topics = self._unique_preserving_order(topics)
        matched_terms = self._unique_preserving_order(
            matched_terms
        )

        return SignalEnrichmentResult(
            keywords=keywords,
            topics=topics,
            matched_terms=matched_terms,
            processing={
                "status": "enriched",
                "method": "deterministic_taxonomy",
                "taxonomy_version": "0.2.0",
            },
        )

    @staticmethod
    def _normalize_text(value: str) -> str:
        value = value.lower()
        value = re.sub(r"\s+", " ", value)
        return value.strip()

    @staticmethod
    def _contains_term(
        normalized_text: str,
        term: str,
    ) -> bool:
        normalized_term = term.lower().strip()

        if not normalized_term:
            return False

        escaped_term = re.escape(normalized_term)

        pattern = rf"(?<!\w){escaped_term}(?!\w)"

        return re.search(
            pattern,
            normalized_text,
            flags=re.IGNORECASE,
        ) is not None

    @staticmethod
    def _clean_terms(
        terms: list[str],
    ) -> list[str]:
        return [
            term.strip()
            for term in terms
            if isinstance(term, str) and term.strip()
        ]

    @staticmethod
    def _unique_preserving_order(
        values: list[str],
    ) -> list[str]:
        result = []
        seen = set()

        for value in values:
            normalized = value.strip().lower()

            if not normalized:
                continue

            if normalized in seen:
                continue

            seen.add(normalized)
            result.append(value.strip())

        return result