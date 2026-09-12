from dataclasses import dataclass, field


@dataclass
class SignalEnrichmentResult:
    """
    Resultado del enriquecimiento semántico determinista de una señal.

    V0 no utiliza modelos externos ni APIs.
    """

    keywords: list[str] = field(default_factory=list)
    topics: list[str] = field(default_factory=list)
    matched_terms: list[str] = field(default_factory=list)
    processing: dict = field(default_factory=dict)