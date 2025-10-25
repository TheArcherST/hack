from __future__ import annotations

from typing import Literal

from pydantic import IPvAnyAddress

from .base import BaseCheckTaskPayload, BaseCheckTaskResult
from .types import CheckTaskTypeEnum


class DNSCheckTaskPayload(BaseCheckTaskPayload):
    type: Literal[CheckTaskTypeEnum.DNS] = CheckTaskTypeEnum.DNS

    ip: IPvAnyAddress
    # and other fields...

    async def perform_check(self) -> DNSCheckTaskResult:
        # do stuff with self.ip and other
        pass


class DNSCheckTaskResult(BaseCheckTaskResult):
    # some results.  will be accessible to frontend
    pass
