from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class DiscoveryRunRequest(BaseModel):
    signal: dict[str, Any]
    brand: dict[str, Any]


class DiscoveryRunResponse(BaseModel):
    discovery: dict[str, Any]
    approval: dict[str, Any] | None


class DiscoveryListResponse(BaseModel):
    discoveries: list[dict[str, Any]]


class DiscoveryApprovalRequest(BaseModel):
    decision: str
    decided_by: str
    notes: str = ""


class DiscoveryApprovalResponse(BaseModel):
    discovery: dict[str, Any]
    approval: dict[str, Any] | None