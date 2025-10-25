from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, status

from hack.core.models import Agent
from hack.core.models.check import Check
from hack.core.services.agent import AgentService
from hack.core.services.checks import CheckService
from hack.core.services.uow_ctl import UoWCtl
from hack.rest_server.schemas.agents import AgentCreateCredentialsDTO, CreateAgentDTO, IssueAgentCreateCredentialsDTO
from hack.rest_server.schemas.checks import (
    CheckDTO,
)
from hack.rest_server.schemas.agents import (
    MyAgentDTO,
)

router = APIRouter(
    prefix="/agents",
)


def generate_compose_file(
        public_key: str,
        ssh_port: int,
):
    return """
services:
  agent:
    build: https://git@git.sourcecraft.dev/lvalue/hack-backend.git#main:python
    command: run-agent-rest-server
    container_name: lvalue-agent
    restart: unless-stopped
  sshd:
    build: https://git@git.sourcecraft.dev/lvalue/hack-backend.git#main:sshd
    container_name: lvalue-sshd
    environment:
      PUBLIC_KEY: "{public_key}"
    ports:
      - "{ssh_port}:22"  # publish SSH only, agent HTTP endpoint is not published
    depends_on:
      - agent
    restart: unless-stopped
""".format(public_key=public_key, ssh_port=ssh_port)


@router.post(
    "/create-credentials",
    status_code=status.HTTP_201_CREATED,
)
@inject
async def issue_agent_create_credentials(
        agent_service: FromDishka[AgentService],
        payload: IssueAgentCreateCredentialsDTO,
) -> AgentCreateCredentialsDTO:
    keypair = await agent_service.issue_keypair()
    return AgentCreateCredentialsDTO(
        public_key=keypair.public_key_openssh,
        compose_file=generate_compose_file(
            public_key=keypair.public_key_openssh,
            ssh_port=payload.port,
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
    keypair = await agent_service.get_keypair_with(
        public_key=payload.public_key,
    )
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
