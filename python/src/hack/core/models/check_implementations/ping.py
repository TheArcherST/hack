from __future__ import annotations

import asyncio
from typing import Literal

from ping3 import ping
from pydantic import IPvAnyAddress, HttpUrl, AnyUrl

from .base import BaseCheckTaskPayload, BaseCheckTaskResult
from .commands import resolve_endpoint
from .type_enum import CheckTaskTypeEnum


class PingCheckTaskPayload(BaseCheckTaskPayload):
    type: Literal[CheckTaskTypeEnum.PING] = CheckTaskTypeEnum.PING
    url: str
    count: int | None = 4

    async def perform_check(self) -> PingCheckTaskResult:
        try:
            resolved_endpoint = await resolve_endpoint(self.url)
            ping_result = [await asyncio.to_thread(ping,  str(resolved_endpoint.some_ip), timeout=10) for i in range(self.count)]
            alive_pings = [i for i in ping_result if i]
            ping_average = sum(alive_pings) / len(alive_pings)
            return PingCheckTaskResult(
                ip=resolved_endpoint.some_ip,
                average_delay=ping_average*100,
                max_delay=max(alive_pings)*100,
                min_delay=min(alive_pings*100),
                live=len(alive_pings),
                total=len(ping_result),
            )
        except Exception as e:
            return PingCheckTaskResult(
                success=False,
                error=str(e)
            )


class PingCheckTaskResult(BaseCheckTaskResult):
    ip: IPvAnyAddress | None = None
    type: Literal[CheckTaskTypeEnum.PING] = CheckTaskTypeEnum.PING
    average_delay: float | None = None  # seconds
    max_delay: float | None = None
    min_delay: float | None = None
    live: int | None = None
    total: int | None = None
    success: bool = False
    error: str | None = None
