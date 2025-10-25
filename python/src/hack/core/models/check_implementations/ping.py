from __future__ import annotations

import asyncio
from typing import Literal

from ping3 import ping
from pydantic import IPvAnyAddress, HttpUrl

from .base import BaseCheckTaskPayload, BaseCheckTaskResult
from .type_enum import CheckTaskTypeEnum


class PingCheckTaskPayload(BaseCheckTaskPayload):
    type: Literal[CheckTaskTypeEnum.PING] = CheckTaskTypeEnum.PING
    host: str
    ip: IPvAnyAddress | None = None
    url: HttpUrl | None = None
    count: int | None = 4

    async def perform_check(self) -> PingCheckTaskResult:
        try:
            # Offload the blocking ping() call to a thread
            ping_result = [await asyncio.to_thread(ping, self.host, timeout=10) for i in range(self.count)]
            alive_pings = [i for i in ping_result if i]
            ping_average = sum(alive_pings) / len(alive_pings)
            return PingCheckTaskResult(
                average_delay=ping_average,
                max_delay=max(alive_pings),
                min_delay=min(alive_pings),
                live=len(alive_pings),
                total=len(ping_result),
            )
        except Exception as e:
            return PingCheckTaskResult(
                success=False,
                error=str(e)
            )


class PingCheckTaskResult(BaseCheckTaskResult):
    type: Literal[CheckTaskTypeEnum.PING] = CheckTaskTypeEnum.PING
    average_delay: float | None = None  # seconds
    max_delay: float | None = None
    min_delay: float | None = None
    live: int | None = None
    total: int | None = None
    success: bool = False
    error: str | None = None
