from uuid import UUID

from .base import BaseDTO

from hack.core.models.check_implementations.dns import DNSCheckTaskPayload, DNSCheckTaskResult


AnyCheckTaskPayload = DNSCheckTaskPayload
AnyCheckTaskResult = DNSCheckTaskResult


class CreateCheckDTO(BaseDTO):
    payload: AnyCheckTaskPayload


class BoundToAgentDTO(BaseDTO):
    name: str


class CheckTask(BaseDTO):
    bound_to_agent: BoundToAgentDTO
    payload: AnyCheckTaskPayload
    result: AnyCheckTaskPayload


class CheckDTO(BaseDTO):
    uid: UUID
    tasks: list[CheckTask]
