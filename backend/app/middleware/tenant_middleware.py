"""
backend/app/middleware/tenant_middleware.py

Extracts the tenant identity for every incoming request and attaches it to
request.state so downstream route handlers, DB session dependencies, and
loggers can all read it from one place — no endpoint should ever accept
tenant_id as a body/query param, because a client could then simply pass
someone else's tenant_id and read their data.

NOTE on production hardening (see docstring at bottom): in production this
header should be *derived from a verified JWT claim*, not trusted as a raw
client-supplied header — see the security note at the end of this file.
"""
from __future__ import annotations

import logging
from uuid import UUID

from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

logger = logging.getLogger("tenant_middleware")

TENANT_HEADER = "X-Tenant-ID"

# Endpoints that legitimately have no tenant context yet (health checks,
# login, docs) — everything else is required to carry the header.
EXEMPT_PATHS = {
    "/v1/health",
    "/v1/auth/login",
    "/v1/auth/register",
    "/docs",
    "/openapi.json",
    "/redoc",
}


class TenantMiddleware(BaseHTTPMiddleware):
    """
    Intercepts every request, extracts X-Tenant-ID, validates it's a
    well-formed UUID, and stores it on request.state.tenant_id.

    Raises 403 Forbidden if the header is missing or malformed on any
    non-exempt path.
    """

    def __init__(self, app: ASGIApp, exempt_paths: set[str] | None = None) -> None:
        super().__init__(app)
        self.exempt_paths = exempt_paths or EXEMPT_PATHS

    async def dispatch(self, request: Request, call_next):
        if request.url.path in self.exempt_paths:
            request.state.tenant_id = None
            return await call_next(request)

        raw_tenant_id = request.headers.get(TENANT_HEADER)

        if not raw_tenant_id:
            logger.warning(
                "Rejected request with missing %s header: %s %s",
                TENANT_HEADER,
                request.method,
                request.url.path,
            )
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": f"Missing required header: {TENANT_HEADER}"},
            )

        try:
            tenant_id = UUID(raw_tenant_id)
        except ValueError:
            logger.warning("Rejected request with malformed %s: %r", TENANT_HEADER, raw_tenant_id)
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": f"Invalid {TENANT_HEADER}: must be a valid UUID"},
            )

        # Attach to request state for downstream use (DB session dependency,
        # logging context, route handlers via `request.state.tenant_id`).
        request.state.tenant_id = tenant_id

        response = await call_next(request)
        # Echo back for client-side debugging/tracing correlation.
        response.headers[TENANT_HEADER] = str(tenant_id)
        return response


"""
SECURITY NOTE (production hardening):

Trusting a raw X-Tenant-ID header is fine for internal/service-to-service
calls behind a private network, but for any client-facing endpoint, an
attacker could simply set X-Tenant-ID to another tenant's UUID and read
their data if there's no independent verification.

Before production, prefer wiring this middleware to also:
  1. Decode and verify the request's JWT (see backend/app/core/security.py).
  2. Confirm the JWT's `tenant_id` claim matches the X-Tenant-ID header
     (or ignore the header entirely and use the JWT claim as the source
     of truth).
  3. Reject the request (401/403) on any mismatch.

This keeps the header useful for local dev/testing/service-to-service
calls while closing the spoofing gap for real end-user traffic.
"""
