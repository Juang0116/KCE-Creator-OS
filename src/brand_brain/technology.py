from dataclasses import dataclass, field
import re


@dataclass
class TechnologyEvidence:
    """
    Semantic technology evidence for Brand Brain V1.2.

    This layer answers:
        1. What technology domain appears?
        2. How central is technology to the signal?
        3. What concrete evidence supports that conclusion?

    It does NOT decide brand relevance.
    """

    technology_domain: str = "none"
    technology_centrality: str = "none"

    matched_terms: list[str] = field(default_factory=list)
    matched_domains: list[str] = field(default_factory=list)

    specific_evidence: list[str] = field(default_factory=list)
    generic_evidence: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "technology_domain": self.technology_domain,
            "technology_centrality": self.technology_centrality,
            "matched_terms": self.matched_terms,
            "matched_domains": self.matched_domains,
            "specific_evidence": self.specific_evidence,
            "generic_evidence": self.generic_evidence,
        }


class TechnologyClassifierV1_2:
    """
    Deterministic semantic technology classifier.

    V1.2 principle:

        SIGNAL
          ↓
        TAXONOMY
          ↓
        DOMAIN
          ↓
        CENTRALITY
          ↓
        BRAND BRAIN

    The classifier intentionally does not calculate brand relevance.

    It distinguishes:

        core
            Technology is central to the subject.

        supporting
            Technology is meaningfully involved, but is not the
            principal subject.

        incidental
            Technology is mentioned peripherally.

        none
            No meaningful technology evidence detected.
    """

    # ------------------------------------------------------------------
    # GENERIC TECHNOLOGY LANGUAGE
    # ------------------------------------------------------------------

    # These terms indicate that technology/AI is present, but by
    # themselves they do NOT establish a concrete technical subject.

    GENERIC_TERMS = {
        "ai",
        "ia",
        "artificial intelligence",
        "inteligencia artificial",
        "generative ai",
        "generative artificial intelligence",
        "chatgpt",
        "gpt",
        "claude",
        "gemini",
        "openai",
        "anthropic",
    }

    # ------------------------------------------------------------------
    # DOMAIN TAXONOMY
    # ------------------------------------------------------------------

    DOMAIN_TERMS = {
        "ai": {
            "ai",
            "ia",
            "artificial intelligence",
            "inteligencia artificial",
            "generative ai",
            "generative artificial intelligence",
            "machine learning",
            "ml",
            "deep learning",
            "dl",
            "computer vision",
            "physical ai",
            "rag",
            "retrieval augmented generation",
            "retrieval-augmented generation",
            "ai agent",
            "ai agents",
            "agents",
            "agentic ai",
            "agentic",
        },
        "software": {
            "software",
            "application",
            "applications",
            "app",
            "apps",
            "platform",
            "platforms",
            "operating system",
            "operating systems",
            "api",
            "apis",
            "backend",
            "frontend",
            "developer",
            "developers",
            "programming",
            "coding",
            "code",
        },
        "developer_tools": {
            "developer tools",
            "developer tool",
            "coding",
            "ai coding",
            "coding agent",
            "coding agents",
            "codex",
            "cursor",
            "github copilot",
            "copilot",
            "pytorch",
            "tensorflow",
            "cuda",
        },
        "hardware": {
            "hardware",
            "gpu",
            "gpus",
            "cpu",
            "cpus",
            "processor",
            "processors",
            "chip",
            "chips",
            "semiconductor",
            "semiconductors",
            "pc",
            "computing hardware",
        },
        "ai_infrastructure": {
            "ai infrastructure",
            "infrastructure",
            "data center",
            "data centers",
            "datacenter",
            "datacenters",
            "compute",
            "computing",
            "training cluster",
            "training clusters",
            "gpu cluster",
            "gpu clusters",
            "ai supercomputer",
            "ai supercomputers",
        },
        "robotics": {
            "robot",
            "robots",
            "robotics",
            "humanoid",
            "humanoids",
            "autonomous robot",
            "autonomous robots",
            "physical ai",
        },
        "cybersecurity": {
            "cybersecurity",
            "cyber security",
            "cyber attack",
            "cyber attacks",
            "cyberattack",
            "cyberattacks",
            "malware",
            "ransomware",
            "phishing",
            "vulnerability",
            "vulnerabilities",
            "exploit",
            "exploits",
            "security research",
            "information security",
        },
        "science_technology": {
            "scientific computing",
            "quantum computing",
            "quantum computer",
            "quantum computers",
            "computational science",
            "theoretical computer science",
            "computer science",
            "machine learning research",
            "ai research",
        },
        "consumer_technology": {
            "smartphone",
            "smartphones",
            "phone",
            "phones",
            "tablet",
            "tablets",
            "wearable",
            "wearables",
            "smartwatch",
            "smartwatches",
            "consumer electronics",
        },
    }

    # ------------------------------------------------------------------
    # HIGH-SPECIFICITY TECHNICAL EVIDENCE
    # ------------------------------------------------------------------

    # These terms represent concrete technologies, systems, frameworks,
    # products or technical concepts.
    #
    # Important:
    # Generic consumer-facing AI products such as ChatGPT, Claude,
    # Gemini and OpenAI are intentionally NOT included here.

    SPECIFIC_ENTITIES = {
        "gpu",
        "gpus",
        "pytorch",
        "tensorflow",
        "cuda",
        "sora",
        "rag",
        "retrieval augmented generation",
        "retrieval-augmented generation",
        "codex",
        "cursor",
        "github copilot",
        "copilot",
        "nvidia",
        "qualcomm",
        "tsmc",
        "amd",
        "intel",
        "dota ai",
        "ai agents",
        "agentic ai",
        "robotics",
        "humanoid",
        "quantum computing",
        "machine learning",
        "deep learning",
        "computer vision",
        "physical ai",
    }

    # Explicit entity → primary domain.
    #
    # This is a semantic priority map, not a scoring system.

    ENTITY_DOMAIN_OVERRIDES = {
        "gpu": "hardware",
        "gpus": "hardware",

        "cuda": "developer_tools",
        "pytorch": "developer_tools",
        "tensorflow": "developer_tools",
        "codex": "developer_tools",
        "cursor": "developer_tools",
        "github copilot": "developer_tools",
        "copilot": "developer_tools",

        "sora": "ai",
        "rag": "ai",
        "retrieval augmented generation": "ai",
        "retrieval-augmented generation": "ai",
        "dota ai": "ai",

        "nvidia": "hardware",
        "qualcomm": "hardware",
        "tsmc": "hardware",
        "amd": "hardware",
        "intel": "hardware",

        "robotics": "robotics",
        "humanoid": "robotics",

        "quantum computing": "science_technology",

        "machine learning": "ai",
        "deep learning": "ai",
        "computer vision": "ai",
        "physical ai": "ai",

        "ai agents": "ai",
        "agentic ai": "ai",
    }

    DOMAIN_PRIORITY = (
        "robotics",
        "cybersecurity",
        "hardware",
        "developer_tools",
        "ai_infrastructure",
        "ai",
        "software",
        "science_technology",
        "consumer_technology",
    )

    # ------------------------------------------------------------------
    # PUBLIC API
    # ------------------------------------------------------------------

    def classify(
        self,
        title: str = "",
        summary: str = "",
        keywords: list[str] | None = None,
        topics: list[str] | None = None,
    ) -> TechnologyEvidence:

        keywords = keywords or []
        topics = topics or []

        title = self._normalize_text(title)
        summary = self._normalize_text(summary)

        metadata_text = self._normalize_text(
            " ".join(
                [
                    *[str(value) for value in keywords if value],
                    *[str(value) for value in topics if value],
                ]
            )
        )

        content_text = f"{title} {summary}".strip()
        all_text = f"{content_text} {metadata_text}".strip()

        specific_matches = self._find_matches(
            all_text,
            self.SPECIFIC_ENTITIES,
        )

        generic_matches = self._find_matches(
            all_text,
            self.GENERIC_TERMS,
        )

        domain_matches = self._find_domain_matches(
            all_text,
        )

        matched_domains = self._ordered_domains(
            domain_matches,
            specific_matches,
        )

        matched_terms = self._ordered_unique(
            [
                *specific_matches,
                *generic_matches,
                *[
                    term
                    for terms in domain_matches.values()
                    for term in terms
                ],
            ]
        )

        specific_evidence = self._ordered_unique(
            specific_matches
        )

        generic_evidence = self._ordered_unique(
            generic_matches
        )

        centrality = self._calculate_centrality(
            content_text=content_text,
            metadata_text=metadata_text,
            specific_matches=specific_matches,
            generic_matches=generic_matches,
            domain_matches=domain_matches,
        )

        primary_domain = self._select_primary_domain(
            matched_domains=matched_domains,
            specific_matches=specific_matches,
        )

        return TechnologyEvidence(
            technology_domain=primary_domain,
            technology_centrality=centrality,
            matched_terms=matched_terms,
            matched_domains=matched_domains,
            specific_evidence=specific_evidence,
            generic_evidence=generic_evidence,
        )

    # ------------------------------------------------------------------
    # MATCHING
    # ------------------------------------------------------------------

    @classmethod
    def _find_matches(
        cls,
        text: str,
        terms: set[str],
    ) -> list[str]:

        matches = []

        for term in sorted(terms):
            if cls._contains_term(text, term):
                matches.append(term)

        return matches

    @classmethod
    def _find_domain_matches(
        cls,
        text: str,
    ) -> dict[str, list[str]]:

        matches = {}

        for domain, terms in cls.DOMAIN_TERMS.items():
            domain_matches = cls._find_matches(
                text,
                terms,
            )

            if domain_matches:
                matches[domain] = domain_matches

        return matches

    # ------------------------------------------------------------------
    # CENTRALITY
    # ------------------------------------------------------------------

    @classmethod
    def _calculate_centrality(
        cls,
        content_text: str,
        metadata_text: str,
        specific_matches: list[str],
        generic_matches: list[str],
        domain_matches: dict[str, list[str]],
    ) -> str:
        """
        Determine how central technology is to the actual content.

        Title/summary have stronger semantic authority than metadata.

        CORE:
            Concrete technical evidence appears in the actual content,
            or multiple independent concrete technology domains establish
            a technical subject.

        SUPPORTING:
            Technology is meaningfully involved, but is not the principal
            subject, or concrete technology evidence exists only in
            metadata.

        INCIDENTAL:
            Only generic AI/product/company language is present.

        NONE:
            No meaningful technology evidence.
        """

        # --------------------------------------------------------------
        # Concrete evidence in actual title/summary.
        # --------------------------------------------------------------

        content_specific = [
            term
            for term in specific_matches
            if cls._contains_term(content_text, term)
        ]

        # --------------------------------------------------------------
        # Generic technology language in actual title/summary.
        # --------------------------------------------------------------

        content_generic = [
            term
            for term in generic_matches
            if cls._contains_term(content_text, term)
        ]

        # --------------------------------------------------------------
        # Concrete domain evidence.
        #
        # Generic terms such as "AI", "ChatGPT", "OpenAI", etc. do not
        # count as concrete domain evidence.
        # --------------------------------------------------------------

        concrete_content_domains = []

        for domain, terms in domain_matches.items():
            concrete_terms = [
                term
                for term in terms
                if term not in cls.GENERIC_TERMS
                and cls._contains_term(content_text, term)
            ]

            if concrete_terms:
                concrete_content_domains.append(domain)

        # --------------------------------------------------------------
        # 1. Explicit concrete technical evidence.
        #
        # GPU, PyTorch, CUDA, Sora, RAG, Codex, robotics, etc.
        # --------------------------------------------------------------

        if content_specific:
            return "core"

        # --------------------------------------------------------------
        # 2. Multiple independent concrete technology domains.
        # --------------------------------------------------------------

        if len(concrete_content_domains) >= 2:
            return "core"

        # --------------------------------------------------------------
        # 3. One concrete technology domain.
        # --------------------------------------------------------------

        if concrete_content_domains:
            if cls._has_technical_subject_context(content_text):
                return "core"

            return "supporting"

        # --------------------------------------------------------------
        # 4. Generic technology language only.
        #
        # Examples:
        #
        #   "AI is changing the future"
        #   "A fisherman uses ChatGPT"
        #   "OpenAI expands its presence"
        #
        # These establish technology presence but NOT a concrete
        # technical subject.
        # --------------------------------------------------------------

        if content_generic:
            return "incidental"

        if generic_matches:
            return "incidental"

        # --------------------------------------------------------------
        # 5. Concrete technology detected only in metadata.
        #
        # Metadata can establish supporting relevance, but should not
        # automatically make the signal core.
        # --------------------------------------------------------------

        metadata_concrete_domains = []

        for domain, terms in domain_matches.items():
            concrete_terms = [
                term
                for term in terms
                if term not in cls.GENERIC_TERMS
                and cls._contains_term(metadata_text, term)
            ]

            if concrete_terms:
                metadata_concrete_domains.append(domain)

        if metadata_concrete_domains:
            return "supporting"

        return "none"

    @classmethod
    def _has_technical_subject_context(
        cls,
        content_text: str,
    ) -> bool:
        """
        Detect whether the technical domain is framed as the subject.

        This uses general semantic framing rather than one-off
        title-specific rules.
        """

        subject_patterns = [
            r"\bhow\b",
            r"\bwhat\b",
            r"\bwhy\b",
            r"\bnew\b",
            r"\bintroducing\b",
            r"\bbuilding\b",
            r"\bbuilds\b",
            r"\bdeveloping\b",
            r"\bdevelops\b",
            r"\blaunches\b",
            r"\busing\b",
            r"\bwith\b",
            r"\bfor\b",
            r"\babout\b",
            r"\bguide\b",
            r"\bresearch\b",
            r"\bexplains?\b",
            r"\badvancing\b",
            r"\btransforming\b",
            r"\btransform\b",
            r"\bimproves?\b",
            r"\bintroduces?\b",
        ]

        return any(
            re.search(
                pattern,
                content_text,
            )
            for pattern in subject_patterns
        )

    # ------------------------------------------------------------------
    # DOMAIN
    # ------------------------------------------------------------------

    @classmethod
    def _select_primary_domain(
        cls,
        matched_domains: list[str],
        specific_matches: list[str],
    ) -> str:

        if not matched_domains:
            return "none"

        # First honor the strongest concrete technical entity.
        #
        # This prevents:
        #
        #   PyTorch + machine learning → AI
        #
        # from incorrectly overriding the explicit PyTorch domain.

        for entity in cls._prioritized_specific_entities(
            specific_matches
        ):
            domain = cls.ENTITY_DOMAIN_OVERRIDES.get(entity)

            if domain:
                return domain

        # Stable fallback when only domain taxonomy evidence exists.

        for domain in cls.DOMAIN_PRIORITY:
            if domain in matched_domains:
                return domain

        return matched_domains[0]

    @classmethod
    def _ordered_domains(
        cls,
        domain_matches: dict[str, list[str]],
        specific_matches: list[str],
    ) -> list[str]:

        domains = []

        for term in cls._prioritized_specific_entities(
            specific_matches
        ):
            domain = cls.ENTITY_DOMAIN_OVERRIDES.get(term)

            if domain and domain not in domains:
                domains.append(domain)

        for domain in cls.DOMAIN_PRIORITY:
            if domain in domain_matches and domain not in domains:
                domains.append(domain)

        return domains

    @classmethod
    def _prioritized_specific_entities(
        cls,
        specific_matches: list[str],
    ) -> list[str]:
        """
        Order concrete entities by semantic specificity.

        Explicit technical tools/products/entities are considered
        stronger domain evidence than broad concepts such as
        machine learning.
        """

        priority = [
            "cuda",
            "pytorch",
            "tensorflow",
            "gpu",
            "gpus",
            "sora",
            "rag",
            "retrieval augmented generation",
            "retrieval-augmented generation",
            "codex",
            "cursor",
            "github copilot",
            "copilot",
            "nvidia",
            "qualcomm",
            "tsmc",
            "amd",
            "intel",
            "dota ai",
            "ai agents",
            "agentic ai",
            "robotics",
            "humanoid",
            "quantum computing",
            "computer vision",
            "physical ai",
            "machine learning",
            "deep learning",
        ]

        result = []

        for term in priority:
            if term in specific_matches:
                result.append(term)

        # Preserve any future terms not yet represented in the
        # explicit priority list.

        for term in specific_matches:
            if term not in result:
                result.append(term)

        return result

    # ------------------------------------------------------------------
    # NORMALIZATION
    # ------------------------------------------------------------------

    @staticmethod
    def _normalize_text(
        value: str,
    ) -> str:

        if not value:
            return ""

        return " ".join(
            str(value).lower().strip().split()
        )

    @classmethod
    def _contains_term(
        cls,
        text: str,
        term: str,
    ) -> bool:

        normalized_text = cls._normalize_text(text)
        normalized_term = cls._normalize_text(term)

        if not normalized_text or not normalized_term:
            return False

        if len(normalized_term.split()) == 1:
            pattern = (
                rf"(?<!\w)"
                rf"{re.escape(normalized_term)}"
                rf"(?!\w)"
            )

            return bool(
                re.search(
                    pattern,
                    normalized_text,
                    flags=re.IGNORECASE,
                )
            )

        return normalized_term in normalized_text

    @staticmethod
    def _ordered_unique(
        values: list[str],
    ) -> list[str]:

        result = []

        for value in values:
            if value and value not in result:
                result.append(value)

        return result