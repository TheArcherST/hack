from fastapi import APIRouter

from . import (
    access,
    checks,
)

router = APIRouter()


router.include_router(access.router)
router.include_router(checks.router)


__all__ = [
    "router",
]
