from __future__ import annotations

import abc
from abc import abstractmethod

from pydantic import BaseModel


class BaseCheckTaskPayload(BaseModel, abc.ABC):
    @abstractmethod
    async def perform_check(self) -> BaseCheckTaskResult:
        raise NotImplementedError


class BaseCheckTaskResult(BaseModel):
    pass
