"""
Health check endpoint for Kubernetes liveness/readiness probes.
Should verify DB and Redis connectivity, not just return 200 unconditionally.
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check():
    # TODO: add DB ping + Redis ping before production use
    return {"status": "ok"}
