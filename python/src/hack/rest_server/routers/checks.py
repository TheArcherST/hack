from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, status

from hack.core.models.check import Check
from hack.core.services.checks import CheckService
from hack.core.services.uow_ctl import UoWCtl
from hack.rest_server.schemas.checks import (
    CreateCheckDTO,
    CheckDTO,
)

router = APIRouter(
    prefix="/checks",
)


@router.post(
    "",
    response_model=CheckDTO,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_check(
        check_service: FromDishka[CheckService],
        uow_ctl: FromDishka[UoWCtl],
        payload: CreateCheckDTO,
) -> Check:
    check = await check_service.create_check(
        payload=payload.payload,
    )
    stream = await streams_service.create_check(
        name=payload.name,
        json_schema=payload.json_schema,
        is_private=payload.is_private,
        is_record_intent=True,
    )
    await uow_ctl.commit()
    return stream


@router.get(
    "/{check_uid}",
    response_model=CheckDTO,
)
@inject
async def get_check(
        streams_service: FromDishka[CheckService],
        check_uid: UUID,
) -> list[Check]:
    streams = await streams_service.get_checks()
    streams = list(streams)
    return streams
