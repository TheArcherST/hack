from .base import BaseDTO

from hack.core.models.check_implementations.dns import DNSCheckTaskPayload, DNSCheckTaskResult


AnyCheckTaskPayload = DNSCheckTaskPayload
AnyCheckTaskResult = DNSCheckTaskResult


class CreateCheckDTO(BaseDTO):
    payload: AnyCheckTaskPayload


class CheckDTO(BaseDTO):
    task_results: list[AnyCheckTaskResult]
