from uuid import UUID

from .base import BaseDTO

from hack.core.models.check_implementations.unions import AnyCheckTaskPayloadType, AnyCheckTaskResultType


class CreateCheckDTO(BaseDTO):
    payload: AnyCheckTaskPayloadType


class BoundToAgentDTO(BaseDTO):
    name: str


class CheckTaskDTO(BaseDTO):
    bound_to_agent: BoundToAgentDTO
    payload: AnyCheckTaskPayloadType
    result: AnyCheckTaskResultType | None


class CheckDTO(BaseDTO):
    uid: UUID
    tasks: list[CheckTaskDTO]
