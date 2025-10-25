from __future__ import annotations

import abc
from abc import abstractmethod

from pydantic import BaseModel

from .types import CheckTaskTypeEnum


class BaseCheckTaskPayload(BaseModel, abc.ABC):
    type: CheckTaskTypeEnum

    @abstractmethod
    async def perform_check(self) -> BaseCheckTaskResult:
        raise NotImplementedError


class BaseCheckTaskResult(BaseModel):
    pass
