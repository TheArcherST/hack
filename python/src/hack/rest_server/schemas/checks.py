from uuid import UUID

from .base import BaseDTO

from ...core.models.check_implementations.unions import AnyCheckTaskPayload


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
