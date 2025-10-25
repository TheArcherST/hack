from uuid import UUID

from .base import BaseDTO

from hack.core.models.check_implementations.unions import AnyCheckTaskPayload, AnyCheckTaskResult


class CreateCheckDTO(BaseDTO):
    payload: AnyCheckTaskPayload


class BoundToAgentDTO(BaseDTO):
    name: str


class CheckTask(BaseDTO):
    bound_to_agent: BoundToAgentDTO
    payload: AnyCheckTaskPayload
    result: AnyCheckTaskResult


class CheckDTO(BaseDTO):
    uid: UUID
    tasks: list[CheckTask]
