"""
Shared tenant_id validation logic — used by both backend/app and analytics/
to avoid duplicating isolation-critical checks in two places.
"""


def validate_tenant_id(tenant_id: str) -> bool:
    """Placeholder: enforce UUID format + existence check against Tenants table."""
    raise NotImplementedError
