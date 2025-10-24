from fastapi import APIRouter

from . import (
    access,
    checks,
)

router = APIRouter()


router.include_router(access.router)


__all__ = [
    "router",
]
