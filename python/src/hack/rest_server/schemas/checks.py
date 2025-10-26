from uuid import UUID
from pydantic import computed_field

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
    failed_count: int

    @computed_field
    @property
    def is_failed(self):
        return self.failed_count >= 3


class CheckDTO(BaseDTO):
    uid: UUID
    tasks: list[CheckTaskDTO]
