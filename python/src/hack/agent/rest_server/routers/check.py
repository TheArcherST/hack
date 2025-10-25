from fastapi import APIRouter

from hack.core.models.check_implementations.unions import AnyCheckTaskPayloadType, AnyCheckTaskResultType
from hack.rest_server.schemas.base import BaseDTO

router = APIRouter()


class PerformCheckDTO(BaseDTO):
    payload: AnyCheckTaskPayloadType


@router.post(
    "/check",
    response_model=AnyCheckTaskResultType,
)
async def perform_check(
        payload: PerformCheckDTO,
):
    result = await payload.payload.perform_check()
    return result
