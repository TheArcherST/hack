from datetime import datetime
from enum import StrEnum
from ipaddress import IPv4Address

from hack.rest_server.schemas.base import BaseDTO


class CreateAgentDTO(BaseDTO):
    ip: IPv4Address
    port: int


class AgentStatus(StrEnum):
    DOWN = "down"
    UP = "up"


class MyAgentDTO(BaseDTO):
    ip: IPv4Address
    port: int
    public_key: str
    compose_file: str
    status: AgentStatus
    created_at: datetime

    @property
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
""".format(public_key=self.public_key, ssh_port=self.port)
