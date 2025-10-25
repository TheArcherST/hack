
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, status

from hack.core.models import Agent
from hack.core.services.agent import AgentService
from hack.core.services.uow_ctl import UoWCtl
from hack.rest_server.schemas.checks import (
    CheckDTO,
)
from hack.rest_server.schemas.agents import (
    MyAgentDTO, CreateAgentDTO,
)

router = APIRouter(
    prefix="/agents",
)


@router.post(
    "",
    response_model=CheckDTO,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_agent(
        agent_service: FromDishka[AgentService],
        uow_ctl: FromDishka[UoWCtl],
        payload: CreateAgentDTO,
) -> Agent:
    keypair = await agent_service.issue_keypair()
    agent = await agent_service.create_agent(
        keypair_id=keypair.id,
        ip=payload.ip,
        port=payload.port,
        rhost="agent",
        rport=8080,
    )
    await uow_ctl.commit()
    return agent


@router.get(
    "/",
    response_model=list[MyAgentDTO],
)
@inject
async def get_my_agents(
        agent_service: FromDishka[AgentService],
) -> list[Agent]:
    streams = await agent_service.get_agents_with()
    streams = list(streams)
    return streams
