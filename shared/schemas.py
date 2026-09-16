"""
shared/schemas.py

Canonical Pydantic schemas shared between the ingestion API (backend/)
and the stream processor (analytics/). Keeping this in `shared/` — rather
than duplicated in both places — is what prevents the two sides of the
pipeline from drifting apart as the project grows.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class EventSchema(BaseModel):
    """
    Canonical schema for every incoming analytics event.

    tenant_id is mandatory on every event — this is the single most
    important field in the whole system, since it's what the tenant
    middleware, RLS policies, and stream partitioning all key off of.
    Never make this Optional.
    """

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    tenant_id: UUID = Field(..., description="Tenant this event belongs to. Mandatory.")
    user_id: Optional[UUID] = Field(
        None, description="User who triggered the event, if applicable (e.g. system events may omit this)."
    )
    event_type: str = Field(
        ..., min_length=1, max_length=100, description="e.g. 'login', 'feature_used', 'api_call'"
    )
    event_payload: dict[str, Any] = Field(
        default_factory=dict, description="Arbitrary event-specific metadata."
    )
    occurred_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="When the event actually happened (client-supplied timestamp, not ingestion time).",
    )

    @field_validator("event_type")
    @classmethod
    def normalize_event_type(cls, v: str) -> str:
        return v.strip().lower().replace(" ", "_")

    @field_validator("occurred_at")
    @classmethod
    def reject_future_timestamps(cls, v: datetime) -> datetime:
        # Guards against clock-skew/bad-actor payloads claiming events "from the future"
        if v.tzinfo is None:
            v = v.replace(tzinfo=timezone.utc)
        if v > datetime.now(timezone.utc):
            raise ValueError("occurred_at cannot be in the future")
        return v


class EventBatch(BaseModel):
    """
    Most real ingestion traffic arrives batched (SDKs buffer client-side
    before flushing) — a batch wrapper avoids N separate HTTP round trips.
    """

    model_config = ConfigDict(extra="forbid")

    events: list[EventSchema] = Field(..., min_length=1, max_length=500)

    @field_validator("events")
    @classmethod
    def enforce_single_tenant_per_batch(cls, events: list[EventSchema]) -> list[EventSchema]:
        # A batch mixing tenant_ids is almost always a client bug or a spoofing
        # attempt — reject it outright rather than silently accepting it.
        tenant_ids = {e.tenant_id for e in events}
        if len(tenant_ids) > 1:
            raise ValueError("All events in a batch must belong to the same tenant_id")
        return events


class EventAck(BaseModel):
    """Response returned to the client after a successful ingestion write."""

    accepted: int
    tenant_id: UUID
    received_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
