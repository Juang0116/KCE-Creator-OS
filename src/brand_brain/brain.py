from src.radar import RadarSignal

from .models import BrandEvaluation


class BrandBrainV0:
    """
    Brand Brain V1.1.

    Evalúa qué tan bien encaja una RadarSignal con una Brand DNA.

    Responsabilidad:
    - evaluar fit con la marca
    - producir una puntuación determinista
    - explicar por qué existe ese fit
    - separar confianza de relevancia
    - distinguir evidencia temática genérica de evidencia específica

    No decide:
    - potencial viral
    - producción
    - valor educativo
    - potencial visual
    - estrategia editorial
    - publicación
    - monetización

    V1.1 principle:
    - Un concepto genérico como "AI" puede detectar pertenencia al
      universo de la marca, pero no basta por sí solo para establecer
      relevancia fuerte.
    - Conceptos específicos como software, agents, GPU, robotics,
      machine learning, etc. aportan evidencia temática adicional.
    - El contexto puede reforzar una coincidencia genérica cuando
      demuestra que la señal realmente trata de tecnología.
    """

    DIMENSION_WEIGHTS = {
        "pillar_fit": 0.25,
        "topic_fit": 0.20,
        "audience_fit": 0.20,
        "brand_promise_fit": 0.20,
        "context_fit": 0.15,
    }

    RELEVANCE_THRESHOLDS = {
        "highly_relevant": 80,
        "relevant": 65,
        "borderline": 45,
    }

    GENERIC_TOPIC_TERMS = {
        "ai",
        "ia",
    }

    SPECIFIC_TOPIC_TERMS = {
        "software",
        "hardware",
        "gpu",
        "pc",
        "creators",
        "robotics",
        "robotics",
        "machine learning",
        "deep learning",
        "artificial intelligence",
        "generative ai",
        "ai applications",
        "ai coding",
        "developer tools",
        "agents",
        "agentic ai",
        "computer vision",
        "chips",
        "cpu",
        "qualcomm",
        "tsmc",
        "ai infrastructure",
    }

    def evaluate(
        self,
        signal: RadarSignal,
        brand: dict,
    ) -> BrandEvaluation:
        brand_id = brand["brand_id"]

        content = brand.get("content", {})
        identity = brand.get("identity", {})
        audience = brand.get("audience", {})

        pillars = content.get("pillars", [])
        topics = content.get("topics", [])
        audience_terms = self._collect_audience_terms(audience)

        signal_terms = self._signal_terms(signal)
        signal_text = self._signal_text(signal)

        matched_pillars = self._match_terms(
            signal_terms,
            pillars,
        )

        matched_topics = self._match_terms(
            signal_terms,
            topics,
        )

        matched_audience_terms = self._match_terms(
            signal_terms,
            audience_terms,
        )

        dimensions = {
            "pillar_fit": self._calculate_pillar_fit(
                matched_pillars,
            ),
            "topic_fit": self._calculate_topic_fit(
                matched_topics,
            ),
            "audience_fit": self._calculate_audience_fit(
                matched_audience_terms,
            ),
            "brand_promise_fit": self._calculate_brand_promise_fit(
                signal_text,
                identity,
            ),
            "context_fit": self._calculate_context_fit(
                signal,
                signal_text,
            ),
        }

        # Brand Promise and Context can reinforce a signal that is
        # already connected to the brand, but they cannot create
        # relevance for a completely unrelated signal.
        has_direct_brand_match = any(
            [
                dimensions["pillar_fit"] > 0,
                dimensions["topic_fit"] > 0,
                dimensions["audience_fit"] > 0,
            ]
        )

        if not has_direct_brand_match:
            dimensions["brand_promise_fit"] = 0.0
            dimensions["context_fit"] = 0.0

        relevance_score = self._calculate_relevance_score(
            dimensions,
        )

        negative_reasons = self._build_negative_reasons(
            signal_text,
            dimensions,
        )

        rule_flags = self._build_rule_flags(
            signal_text,
            dimensions,
            matched_pillars,
            matched_topics,
            signal_terms,
        )

        positive_reasons = self._build_positive_reasons(
            matched_pillars,
            matched_topics,
            matched_audience_terms,
            dimensions,
        )

        relevance_level = self._get_relevance_level(
            relevance_score,
            matched_pillars,
            matched_topics,
        )

        # The relevance level must reflect the same V1.1 gate used by
        # _is_relevant(). A generic AI-only signal can have a high raw
        # weighted score because AI matches several brand fields, but
        # without specific evidence or strong context it is only
        # borderline rather than genuinely relevant.
        if self._is_generic_ai_only(
            matched_pillars,
            matched_topics,
            matched_audience_terms,
        ):
            if not self._has_specific_topic_evidence(
                signal_terms,
                matched_topics,
            ) and dimensions["context_fit"] < 8:
                relevance_level = "borderline"

        relevant = self._is_relevant(
            relevance_score,
            matched_pillars,
            matched_topics,
            matched_audience_terms,
            dimensions,
            signal_terms,
        )

        confidence = self._calculate_confidence(
            matched_pillars,
            matched_topics,
            matched_audience_terms,
            dimensions,
        )

        reason = self._build_reason(
            relevance_score,
            relevance_level,
            matched_pillars,
            matched_topics,
        )

        return BrandEvaluation(
            brand_id=brand_id,
            signal_id=signal.signal_id,
            relevant=relevant,
            relevance_score=relevance_score,
            matched_pillars=matched_pillars,
            matched_topics=matched_topics,
            reason=reason,
            rule_flags=rule_flags,
            confidence=confidence,
            relevance_level=relevance_level,
            dimensions=dimensions,
            positive_reasons=positive_reasons,
            negative_reasons=negative_reasons,
        )

    # ------------------------------------------------------------------
    # DIMENSIONS
    # ------------------------------------------------------------------

    @staticmethod
    def _calculate_pillar_fit(
        matched_pillars: list[str],
    ) -> float:
        if not matched_pillars:
            return 0.0

        if len(matched_pillars) >= 2:
            return 10.0

        return 7.0

    @staticmethod
    def _calculate_topic_fit(
        matched_topics: list[str],
    ) -> float:
        if not matched_topics:
            return 0.0

        if len(matched_topics) >= 2:
            return 10.0

        return 7.0

    @staticmethod
    def _calculate_audience_fit(
        matched_audience_terms: list[str],
    ) -> float:
        if not matched_audience_terms:
            return 0.0

        if len(matched_audience_terms) >= 2:
            return 10.0

        return 7.0

    def _calculate_brand_promise_fit(
        self,
        signal_text: str,
        identity: dict,
    ) -> float:
        value_proposition = identity.get(
            "value_proposition",
            "",
        )

        if not value_proposition:
            return 0.0

        signal_normalized = self._normalize_text(
            signal_text,
        )

        proposition_normalized = self._normalize_text(
            value_proposition,
        )

        concept_groups = {
            "clarity": {
                "explain",
                "explains",
                "explanation",
                "clear",
                "clearly",
                "understand",
                "understanding",
                "accessible",
                "simple",
                "explicar",
                "explica",
                "explicación",
                "claro",
                "clara",
                "claramente",
                "entender",
                "entiende",
                "comprender",
                "comprensible",
                "accesible",
                "sencillo",
                "sencilla",
            },
            "learning": {
                "learn",
                "learning",
                "teach",
                "teaching",
                "education",
                "educational",
                "aprender",
                "aprendizaje",
                "enseñar",
                "enseñanza",
                "educación",
                "educativo",
                "educativa",
            },
            "technology": {
                "technology",
                "technologies",
                "tech",
                    "software",
                "hardware",
                "robotics",
                "gpu",
                "tecnología",
                "tecnologias",
                "tecnologías",
                "tecnología",
                "ia",
                "software",
                "hardware",
                "robótica",
                "gpu",
            },
        }

        matched_concepts = 0

        for terms in concept_groups.values():
            signal_match = any(
                self._contains_term(
                    signal_normalized,
                    term,
                )
                for term in terms
            )

            proposition_match = any(
                self._contains_term(
                    proposition_normalized,
                    term,
                )
                for term in terms
            )

            if signal_match and proposition_match:
                matched_concepts += 1

        if matched_concepts >= 2:
            return 10.0

        if matched_concepts == 1:
            return 7.0

        return 0.0

    @staticmethod
    def _calculate_context_fit(
        signal: RadarSignal,
        signal_text: str,
    ) -> float:
        normalized = BrandBrainV0._normalize_text(
            signal_text,
        )

        generic_contexts = {
            "team update",
            "company update",
            "weekly update",
            "internal update",
        }

        if any(
            context in normalized
            for context in generic_contexts
        ):
            return 2.0

        concrete_terms = {
            "acquire",
            "acquires",
            "acquisition",
            "launch",
            "launches",
            "launched",
            "new",
            "research",
            "development",
            "developers",
            "infrastructure",
            "platform",
            "system",
            "software",
            "technology",
            "transform",
            "transforms",
            "modernize",
            "modernizes",
            "scientific",
            "coding",
            "agents",
            "agentic",
            "gpu",
            "hardware",
            "machine learning",
            "deep learning",
            "robotics",
            "robot",
            "artificial intelligence",
            "generative ai",
            "adquire",
            "adquiere",
            "adquisición",
            "lanzamiento",
            "nuevo",
            "nueva",
            "investigación",
            "desarrollo",
            "desarrolladores",
            "infraestructura",
            "plataforma",
            "sistema",
            "tecnología",
            "transforma",
            "moderniza",
            "científico",
            "científica",
            "agentes",
        }

        tokens = BrandBrainV0._tokenize(
            normalized,
        )

        matches = len(
            tokens.intersection(
                {
                    term
                    for term in concrete_terms
                    if " " not in term
                }
            )
        )

        phrase_matches = sum(
            1
            for term in concrete_terms
            if " " in term and term in normalized
        )

        total_matches = matches + phrase_matches

        if total_matches >= 3:
            return 10.0

        if total_matches == 2:
            return 8.0

        if total_matches == 1:
            return 6.0

        if signal.title and signal.summary:
            return 0.0

        if signal.title:
            return 0.0

        return 0.0

    # ------------------------------------------------------------------
    # SCORE
    # ------------------------------------------------------------------

    def _calculate_relevance_score(
        self,
        dimensions: dict[str, float],
    ) -> float:
        weighted_score = sum(
            dimensions[name] * weight
            for name, weight in self.DIMENSION_WEIGHTS.items()
        )

        return round(
            weighted_score * 10,
            2,
        )

    # ------------------------------------------------------------------
    # MATCHING
    # ------------------------------------------------------------------

    @staticmethod
    def _match_terms(
        signal_terms: list[str],
        brand_terms: list[str],
    ) -> list[str]:
        signal_normalized = {
            BrandBrainV0._normalize_text(term)
            for term in signal_terms
            if isinstance(term, str) and term.strip()
        }

        matches = []

        for brand_term in brand_terms:
            if not isinstance(brand_term, str):
                continue

            normalized = BrandBrainV0._normalize_text(
                brand_term,
            )

            if normalized in signal_normalized:
                matches.append(brand_term)

        return matches

    @staticmethod
    def _collect_audience_terms(
        audience: dict,
    ) -> list[str]:
        terms = []

        terms.extend(audience.get("interests", []))
        terms.extend(audience.get("problems", []))
        terms.extend(audience.get("desires", []))

        return terms

    @staticmethod
    def _signal_terms(
        signal: RadarSignal,
    ) -> list[str]:
        return list(
            dict.fromkeys(
                [
                    *signal.keywords,
                    *signal.topics,
                ]
            )
        )

    @staticmethod
    def _signal_text(
        signal: RadarSignal,
    ) -> str:
        return " ".join(
            [
                signal.title or "",
                signal.summary or "",
                " ".join(signal.keywords),
                " ".join(signal.topics),
            ]
        )

    # ------------------------------------------------------------------
    # EVIDENCE CLASSIFICATION
    # ------------------------------------------------------------------

    @classmethod
    def _has_specific_topic_evidence(
        cls,
        signal_terms: list[str],
        matched_topics: list[str],
    ) -> bool:
        """
        Determina si existe evidencia temática más específica que el
        concepto genérico "AI".

        Se inspeccionan tanto los topics que coinciden directamente con
        la Brand DNA como los términos detectados por Signal Enrichment.
        Esto permite que conceptos específicos descubiertos por el
        taxonomy (por ejemplo software, agents, GPU o robotics)
        refuercen la relevancia aunque la Brand DNA no los enumere
        explícitamente como topic.
        """
        normalized_evidence = {
            cls._normalize_text(value)
            for value in [*signal_terms, *matched_topics]
            if isinstance(value, str) and value.strip()
        }

        specific_terms = {
            cls._normalize_text(term)
            for term in cls.SPECIFIC_TOPIC_TERMS
        }

        return any(
            term in specific_terms
            for term in normalized_evidence
            if term not in cls.GENERIC_TOPIC_TERMS
        )

    @classmethod
    def _is_generic_ai_only(
        cls,
        matched_pillars: list[str],
        matched_topics: list[str],
        matched_audience_terms: list[str],
    ) -> bool:
        """
        True cuando la evidencia directa está dominada únicamente
        por AI/IA y no existe un concepto específico adicional.

        No considera el contexto todavía; el contexto se evalúa
        separadamente para permitir que una señal genérica pueda
        superar el filtro si realmente contiene suficiente evidencia.
        """
        normalized_pillars = {
            cls._normalize_text(value)
            for value in matched_pillars
        }

        normalized_topics = {
            cls._normalize_text(value)
            for value in matched_topics
        }

        normalized_audience = {
            cls._normalize_text(value)
            for value in matched_audience_terms
        }

        pillar_is_generic_ai = (
            normalized_pillars
            and normalized_pillars.issubset(
                cls.GENERIC_TOPIC_TERMS
            )
        )

        topics_are_generic_ai = (
            normalized_topics
            and normalized_topics.issubset(
                cls.GENERIC_TOPIC_TERMS
            )
        )

        audience_has_specific_evidence = any(
            term not in cls.GENERIC_TOPIC_TERMS
            for term in normalized_audience
        )

        return (
            bool(pillar_is_generic_ai)
            and bool(topics_are_generic_ai)
            and not audience_has_specific_evidence
        )

    # ------------------------------------------------------------------
    # REASONS / FLAGS
    # ------------------------------------------------------------------

    @staticmethod
    def _build_positive_reasons(
        matched_pillars: list[str],
        matched_topics: list[str],
        matched_audience_terms: list[str],
        dimensions: dict[str, float],
    ) -> list[str]:
        reasons = []

        if matched_pillars:
            reasons.append(
                "Coincide con pilares de contenido: "
                + ", ".join(matched_pillars)
                + "."
            )

        if matched_topics:
            reasons.append(
                "Coincide con topics de la marca: "
                + ", ".join(matched_topics)
                + "."
            )

        if matched_audience_terms:
            reasons.append(
                "Presenta coincidencias con la audiencia: "
                + ", ".join(matched_audience_terms)
                + "."
            )

        if dimensions["brand_promise_fit"] > 0:
            reasons.append(
                "El contexto es compatible con la propuesta "
                "de valor de la marca."
            )

        if dimensions["context_fit"] >= 8:
            reasons.append(
                "La señal contiene contexto suficientemente "
                "específico."
            )

        return reasons

    @staticmethod
    def _build_negative_reasons(
        signal_text: str,
        dimensions: dict[str, float],
    ) -> list[str]:
        reasons = []

        if (
            dimensions["pillar_fit"] == 0
            and dimensions["topic_fit"] == 0
            and dimensions["audience_fit"] == 0
        ):
            reasons.append(
                "No se encontraron coincidencias temáticas "
                "con la marca."
            )

        normalized = BrandBrainV0._normalize_text(
            signal_text,
        )

        generic_contexts = {
            "team update",
            "company update",
            "weekly update",
            "internal update",
        }

        for context in generic_contexts:
            if context in normalized:
                reasons.append(
                    f"El contexto es demasiado genérico: {context}."
                )

        return reasons

    @classmethod
    def _build_rule_flags(
        cls,
        signal_text: str,
        dimensions: dict[str, float],
        matched_pillars: list[str],
        matched_topics: list[str],
        signal_terms: list[str],
    ) -> list[str]:
        flags = []

        if dimensions["pillar_fit"] == 0:
            flags.append("no_pillar_match")

        if dimensions["topic_fit"] == 0:
            flags.append("no_topic_match")

        if dimensions["audience_fit"] == 0:
            flags.append("no_audience_match")

        if dimensions["brand_promise_fit"] == 0:
            flags.append("no_brand_promise_match")

        if dimensions["context_fit"] <= 2:
            flags.append("weak_context")

        if not cls._has_specific_topic_evidence(
            signal_terms,
            matched_topics,
        ):
            flags.append("no_specific_topic_evidence")

        if cls._is_generic_ai_only(
            matched_pillars,
            matched_topics,
            [],
        ):
            flags.append("generic_ai_evidence")

        normalized = cls._normalize_text(
            signal_text,
        )

        generic_contexts = {
            "team update",
            "company update",
            "weekly update",
            "internal update",
        }

        if any(
            context in normalized
            for context in generic_contexts
        ):
            flags.append("generic_context")

        return flags

    # ------------------------------------------------------------------
    # RELEVANCE
    # ------------------------------------------------------------------

    @classmethod
    def _get_relevance_level(
        cls,
        score: float,
        matched_pillars: list[str],
        matched_topics: list[str],
    ) -> str:
        if score >= cls.RELEVANCE_THRESHOLDS["highly_relevant"]:
            return "highly_relevant"

        if score >= cls.RELEVANCE_THRESHOLDS["relevant"]:
            return "relevant"

        if score >= cls.RELEVANCE_THRESHOLDS["borderline"]:
            return "borderline"

        # Preserve a meaningful distinction for a direct core
        # pillar/topic match even when other evidence is sparse.
        if matched_pillars or matched_topics:
            return "borderline"

        return "irrelevant"

    @classmethod
    def _is_relevant(
        cls,
        score: float,
        matched_pillars: list[str],
        matched_topics: list[str],
        matched_audience_terms: list[str],
        dimensions: dict[str, float],
        signal_terms: list[str],
    ) -> bool:
        """
        Establishes Brand Brain relevance.

        V1.1 change:
        A generic AI-only match is not enough by itself.

        Specific topic evidence, a strong score, or a non-generic
        direct brand match can establish relevance.

        This deliberately does not make "borderline" synonymous with
        "relevant". Opportunity Engine remains responsible for
        deciding whether a relevant signal is worth producing.
        """
        generic_ai_only = cls._is_generic_ai_only(
            matched_pillars,
            matched_topics,
            matched_audience_terms,
        )

        has_specific_topic = cls._has_specific_topic_evidence(
            signal_terms,
            matched_topics,
        )

        # Generic AI/IA evidence is intentionally filtered before the
        # score threshold. Otherwise the weighted dimensions could let
        # a generic AI-only signal become relevant simply because AI
        # appears in several brand fields.
        if generic_ai_only:
            return (
                has_specific_topic
                or dimensions["context_fit"] >= 8
            )

        # Strong score is sufficient for non-generic evidence.
        if score >= 65:
            return True

        # Non-generic direct brand matches can remain relevant even
        # when their score is below the 45-point borderline threshold.
        if matched_pillars or matched_topics:
            return True

        return score >= 45

    # ------------------------------------------------------------------
    # CONFIDENCE
    # ------------------------------------------------------------------

    @staticmethod
    def _calculate_confidence(
        matched_pillars: list[str],
        matched_topics: list[str],
        matched_audience_terms: list[str],
        dimensions: dict[str, float],
    ) -> float:
        evidence_count = sum(
            [
                len(matched_pillars),
                len(matched_topics),
                len(matched_audience_terms),
                int(dimensions["brand_promise_fit"] > 0),
                int(dimensions["context_fit"] > 0),
            ]
        )

        if evidence_count >= 6:
            return 0.95

        if evidence_count >= 4:
            return 0.90

        if evidence_count >= 2:
            return 0.80

        if evidence_count == 1:
            return 0.60

        return 0.20

    # ------------------------------------------------------------------
    # PRESENTATION
    # ------------------------------------------------------------------

    @staticmethod
    def _build_reason(
        relevance_score: float,
        relevance_level: str,
        matched_pillars: list[str],
        matched_topics: list[str],
    ) -> str:
        parts = []

        if matched_pillars:
            parts.append(
                "pilares: " + ", ".join(matched_pillars)
            )

        if matched_topics:
            parts.append(
                "topics: " + ", ".join(matched_topics)
            )

        if parts:
            detail = " y ".join(parts)
        else:
            detail = "sin coincidencias directas"

        return (
            f"Relevancia {relevance_level} "
            f"({relevance_score}/100): {detail}."
        )

    # ------------------------------------------------------------------
    # NORMALIZATION
    # ------------------------------------------------------------------

    @staticmethod
    def _normalize_text(
        value: str,
    ) -> str:
        return " ".join(
            value.lower().strip().split()
        )

    @staticmethod
    def _tokenize(
        value: str,
    ) -> set[str]:
        normalized = BrandBrainV0._normalize_text(
            value,
        )

        punctuation = ",.:;!?()-/"

        for character in punctuation:
            normalized = normalized.replace(
                character,
                " ",
            )

        return {
            token
            for token in normalized.split()
            if token
        }

    @staticmethod
    def _contains_term(
        text: str,
        term: str,
    ) -> bool:
        normalized_text = BrandBrainV0._normalize_text(
            text,
        )

        normalized_term = BrandBrainV0._normalize_text(
            term,
        )

        if not normalized_term:
            return False

        return (
            normalized_term in
            BrandBrainV0._tokenize(normalized_text)
            or normalized_term in normalized_text
        )