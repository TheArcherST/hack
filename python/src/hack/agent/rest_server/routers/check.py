from fastapi import APIRouter

from hack.core.models.check_implementations.unions import AnyCheckTaskPayloadType

router = APIRouter()


@router.post(
    "/check",
    response_model=AnyCheckTaskPayloadType,
)
async def perform_check(
        payload: AnyCheckTaskPayloadType,
):
    result = await payload.perform_check()
    return result
