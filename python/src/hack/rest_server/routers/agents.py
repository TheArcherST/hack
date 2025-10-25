from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, status

from hack.core.models import Agent
from hack.core.models.check import Check
from hack.core.services.agent import AgentService
from hack.core.services.checks import CheckService
from hack.core.services.uow_ctl import UoWCtl
from hack.rest_server.schemas.agents import AgentCreateCredentialsDTO, CreateAgentDTO
from hack.rest_server.schemas.checks import (
    CheckDTO,
)

router = APIRouter(
    prefix="/agents",
)


def generate_compose_file(
        public_key: str,
):
    return """
services:
  agent:
    build: https://sourcecraft.dev/lvalue/hack-backend#python
    command: run-agent-rest-server
    container_name: lvalue-agent
    restart: unless-stopped
  sshd:
    build: https://sourcecraft.dev/lvalue/hack-backend#sshd
    container_name: lvalue-sshd
    environment:
      PUBLIC_KEY: "{public_key}"
    ports:
      - "2222:22"  # publish SSH only, agent HTTP endpoint is not published
    depends_on:
      - agent
    restart: unless-stopped
""".format(public_key=public_key)


@router.post(
    "/create-credentials",
)
@inject
async def issue_create_credentials(
     agent_service: FromDishka[AgentService],
) -> AgentCreateCredentialsDTO:
    keypair = await agent_service.issue_keypair()
    return AgentCreateCredentialsDTO(
        public_key=keypair.public_key_openssh,
        compose_file=generate_compose_file(
            public_key=keypair.public_key_openssh,
        ),
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
    agent = await agent_service.create_agent(
        keypair_id=payload.keypair_id,
        ip=payload.ipv4,
        rhost="agent",
        rport=8080,
    )
    await uow_ctl.commit()
    return agent


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
