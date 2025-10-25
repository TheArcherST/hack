from datetime import datetime
from ipaddress import IPv4Address

from pydantic import field_serializer, field_validator, computed_field

from hack.core.models.agent import AgentStatus, Agent
from hack.rest_server.schemas.base import BaseDTO


class CreateAgentDTO(BaseDTO):
    name: str
    ip: IPv4Address
    port: int


class UpdateAgentDTO(BaseDTO):
    name: str
    ip: IPv4Address
    port: int
    is_suspended: bool


class MyKeypairDTO(BaseDTO):
    public_key_openssh: str


class MyAgentDTO(BaseDTO):
    id: int
    name: str
    ip: IPv4Address
    port: int
    status: AgentStatus
    is_suspended: bool
    created_at: datetime
    keypair: MyKeypairDTO

    @computed_field(return_type=str)
    def compose_file(
            self,
    ):
        return """\
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
    restart: unless-stopped\
""".format(public_key=self.keypair.public_key_openssh, ssh_port=self.port)
