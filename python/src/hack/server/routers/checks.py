from collections.abc import Iterable

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException, status

from hack.core.models.check import Check
from hack.core.services.checks import CheckService
from hack.core.services.uow_ctl import UoWCtl
from hack.server.schemas.checks import (
    CreateStreamDTO,
    CreateStreamPropositionDTO,
    StreamDTO,
    StreamPropositionDTO,
)

router = APIRouter(
    prefix="/streams",
)


@router.post(
    "",
    response_model=StreamDTO,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_check(
        streams_service: FromDishka[CheckService],
        uow_ctl: FromDishka[UoWCtl],
        payload: CreateStreamDTO,
) -> Check:
    stream = await streams_service.create_check(
        name=payload.name,
        json_schema=payload.json_schema,
        is_private=payload.is_private,
        is_record_intent=True,
    )
    await uow_ctl.commit()
    return stream


@router.get(
    "",
    response_model=list[StreamDTO],
)
@inject
async def get_streams(
        streams_service: FromDishka[CheckService],
) -> list[Check]:
    streams = await streams_service.get_streams()
    streams = list(streams)
    return streams
