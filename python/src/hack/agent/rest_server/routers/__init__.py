from fastapi import APIRouter

from . import (
    healthcheck,
    check,
)


router = APIRouter()


router.include_router(healthcheck.router)
router.include_router(check.router)
