from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from src.application import DiscoveryFacadeV0
from src.radar import RadarSignal

from .dependencies import get_discovery
from .models import (
    DiscoveryListResponse,
    DiscoveryRunRequest,
    DiscoveryRunResponse,
)


router = APIRouter(
    prefix="/discovery",
    tags=["discovery"],
)


def _build_signal(data: dict) -> RadarSignal:
    source = data.get("source", {})
    signal = data.get("signal", {})
    relevance = data.get("relevance", {})
    processing = data.get("processing", {})

    return RadarSignal(
        signal_id=data["signal_id"],
        detected_at=data["detected_at"],
        radar_version=data["radar_version"],
        source_type=source.get("type", ""),
        platform=source.get("platform", ""),
        url=source.get("url"),
        author=source.get("author"),
        published_at=source.get("published_at"),
        title=signal.get("title", ""),
        summary=signal.get("summary", ""),
        keywords=signal.get("keywords", []),
        topics=signal.get("topics", []),
        language=signal.get("language", "es"),
        evidence=data.get("evidence", {}),
        niches=relevance.get("niches", []),
        relevance_reason=relevance.get(
            "relevance_reason",
            "",
        ),
        status=processing.get(
            "status",
            "detected",
        ),
        confidence=processing.get(
            "confidence",
            0.0,
        ),
        processed_at=processing.get(
            "processed_at"
        ),
    )


@router.post(
    "",
    response_model=DiscoveryRunResponse,
    status_code=status.HTTP_201_CREATED,
)
def run_discovery(
    request: DiscoveryRunRequest,
    discovery: DiscoveryFacadeV0 = Depends(get_discovery),
) -> DiscoveryRunResponse:
    signal = _build_signal(request.signal)

    package = discovery.run(
        signal=signal,
        brand=request.brand,
    )

    return DiscoveryRunResponse(
        discovery=package.discovery.to_dict(),
        approval=(
            package.approval.to_dict()
            if package.approval is not None
            else None
        ),
    )


@router.get(
    "",
    response_model=DiscoveryListResponse,
)
def list_discoveries(
    discovery: DiscoveryFacadeV0 = Depends(get_discovery),
) -> DiscoveryListResponse:
    packages = discovery.list_all()

    return DiscoveryListResponse(
        discoveries=[
            package.discovery.to_dict()
            for package in packages
        ]
    )


@router.get(
    "/{discovery_id}",
    response_model=DiscoveryRunResponse,
)
def get_discovery(
    discovery_id: str,
    discovery: DiscoveryFacadeV0 = Depends(get_discovery),
) -> DiscoveryRunResponse:
    package = discovery.get(discovery_id)

    if package is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Discovery not found.",
        )

    return DiscoveryRunResponse(
        discovery=package.discovery.to_dict(),
        approval=(
            package.approval.to_dict()
            if package.approval is not None
            else None
        ),
    )