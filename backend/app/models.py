"""
backend/app/models.py

SQLAlchemy models for the core multi-tenant schema: Tenant, User,
ActivityLog, Subscription. (Metric is intentionally excluded from
TenantMixin inheritance discussion below — see note at the bottom.)

NOTE: This consolidates what the initial scaffold split into
backend/app/models/{tenant,user,activity_log,subscription}.py into a
single file, per this request. For a growing codebase you'd typically
split these back out once the file gets large — the TenantMixin below
would move to backend/app/models/mixins.py.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column, relationship


class Base(DeclarativeBase):
    pass


def _uuid_pk() -> Mapped[uuid.UUID]:
    return mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


class TimestampMixin:
    """Standard created_at/updated_at columns, reused across every model."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class TenantMixin:
    """
    Mandatory mixin for every tenant-scoped table.

    Every model that mixes this in automatically gets:
      - a tenant_id column, FK'd to tenants.tenant_id
      - an index on tenant_id (nearly every query filters by it)

    This is the ORM-level half of the isolation strategy from the PRD —
    the other half is the PostgreSQL Row-Level Security policy on each
    of these tables (see docs/architecture.md), which is what actually
    prevents a query from leaking cross-tenant data even if application
    code forgets to filter by tenant_id.

    IMPORTANT: Tenant itself does NOT use this mixin — a tenant doesn't
    belong to another tenant. Only use TenantMixin on tables that
    represent tenant-owned data.
    """

    @declared_attr
    def tenant_id(cls) -> Mapped[uuid.UUID]:
        return mapped_column(
            PG_UUID(as_uuid=True),
            ForeignKey("tenants.tenant_id", ondelete="CASCADE"),
            nullable=False,
        )

    @declared_attr
    def __table_args__(cls):
        # Composite index pattern: (tenant_id, <primary access pattern col>)
        # is added per-model below where a second natural filter column
        # exists (e.g. occurred_at on ActivityLog); this base index covers
        # the fallback "just filter by tenant" case for every model.
        return (Index(f"ix_{cls.__tablename__}_tenant_id", "tenant_id"),)


class Tenant(TimestampMixin, Base):
    """The top-level tenant (customer company). Does NOT use TenantMixin."""

    __tablename__ = "tenants"

    tenant_id: Mapped[uuid.UUID] = _uuid_pk()
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    plan_tier: Mapped[str] = mapped_column(String(50), nullable=False, default="free")
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="active")

    __table_args__ = (
        CheckConstraint("status in ('active','suspended','churned')", name="ck_tenant_status"),
    )

    users: Mapped[list["User"]] = relationship(back_populates="tenant", cascade="all, delete-orphan")
    activity_logs: Mapped[list["ActivityLog"]] = relationship(
        back_populates="tenant", cascade="all, delete-orphan"
    )
    subscriptions: Mapped[list["Subscription"]] = relationship(
        back_populates="tenant", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Tenant {self.tenant_id} {self.company_name!r} tier={self.plan_tier}>"


class User(TenantMixin, TimestampMixin, Base):
    __tablename__ = "users"

    user_id: Mapped[uuid.UUID] = _uuid_pk()
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False, default="member")

    tenant: Mapped["Tenant"] = relationship(back_populates="users")
    activity_logs: Mapped[list["ActivityLog"]] = relationship(back_populates="user")

    __table_args__ = (
        # Email must be unique *within* a tenant, not globally — two
        # different tenants may legitimately have a user with the same
        # email (e.g. a consultant working with multiple clients).
        UniqueConstraint("tenant_id", "email", name="uq_user_tenant_email"),
        CheckConstraint("role in ('admin','member','viewer')", name="ck_user_role"),
        Index("ix_users_tenant_id", "tenant_id"),
    )

    def __repr__(self) -> str:
        return f"<User {self.user_id} {self.email!r} tenant={self.tenant_id}>"


class ActivityLog(TenantMixin, Base):
    """
    High-volume ingestion target. No TimestampMixin here on purpose —
    occurred_at (below) is the meaningful timestamp; a separate
    created_at would just duplicate it for an append-only log table.
    """

    __tablename__ = "activity_logs"

    log_id: Mapped[uuid.UUID] = _uuid_pk()
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True
    )
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    event_payload: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    tenant: Mapped["Tenant"] = relationship(back_populates="activity_logs")
    user: Mapped["User | None"] = relationship(back_populates="activity_logs")

    __table_args__ = (
        # This is the index that matters most in the whole schema — almost
        # every dashboard/analytics query filters by tenant + time window.
        Index("ix_activity_logs_tenant_occurred", "tenant_id", "occurred_at"),
    )

    def __repr__(self) -> str:
        return f"<ActivityLog {self.log_id} tenant={self.tenant_id} type={self.event_type!r}>"


class Subscription(TenantMixin, TimestampMixin, Base):
    __tablename__ = "subscriptions"

    subscription_id: Mapped[uuid.UUID] = _uuid_pk()
    plan_id: Mapped[str] = mapped_column(String(50), nullable=False)
    mrr_cents: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    renewal_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="active")

    tenant: Mapped["Tenant"] = relationship(back_populates="subscriptions")

    __table_args__ = (
        CheckConstraint("mrr_cents >= 0", name="ck_subscription_mrr_nonnegative"),
        CheckConstraint(
            "status in ('active','past_due','cancelled')", name="ck_subscription_status"
        ),
        Index("ix_subscriptions_tenant_renewal", "tenant_id", "renewal_date"),
    )

    def __repr__(self) -> str:
        return f"<Subscription {self.subscription_id} tenant={self.tenant_id} status={self.status}>"


# NOTE: `Metric` was intentionally left out of this file's scope (the
# request only asked for Tenant, User, ActivityLog, Subscription). It
# belongs in the same file/pattern — TenantMixin + a composite
# (tenant_id, metric_name, computed_at) index — add it here when you
# wire up the scoring pipeline from analytics/scoring/churn_model.py.
