from datetime import datetime
from enum import StrEnum
from ipaddress import IPv4Address

from hack.rest_server.schemas.base import BaseDTO


class IssueAgentCreateCredentialsDTO(BaseDTO):
    port: int


class AgentCreateCredentialsDTO(BaseDTO):
    public_key: str
    compose_file: str


class CreateAgentDTO(BaseDTO):
    public_key: str
    ip: IPv4Address
    port: int


class AgentStatus(StrEnum):
    DOWN = "down"
    UP = "up"


class MyAgentDTO(BaseDTO):
    ip: IPv4Address
    port: int
    public_key: str
    status: AgentStatus
    created_at: datetime
