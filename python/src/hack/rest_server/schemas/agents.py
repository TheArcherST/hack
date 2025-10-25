from ipaddress import IPv4Address

from hack.rest_server.schemas.base import BaseDTO


class AgentCreateCredentialsDTO(BaseDTO):
    public_key: str
    compose_file: str


class CreateAgentDTO(BaseDTO):
    public_key: str
    ip: IPv4Address
