from __future__ import annotations

import asyncio
from typing import Literal

from ping3 import ping
from pydantic import IPvAnyAddress

from .base import BaseCheckTaskPayload, BaseCheckTaskResult
from .type_enum import CheckTaskTypeEnum


class PingCheckTaskPayload(BaseCheckTaskPayload):
    type: Literal[CheckTaskTypeEnum.PING] = CheckTaskTypeEnum.PING
    host: str
    ip: IPvAnyAddress | None = None

    async def perform_check(self) -> PingCheckTaskResult:
        try:
            # Offload the blocking ping() call to a thread
            response_time = await asyncio.to_thread(ping, self.host, timeout=2)

            if response_time is not None:
                return PingCheckTaskResult(
                    response_time=response_time,
                    success=True
                )
            else:
                return PingCheckTaskResult(
                    response_time=None,
                    success=False,
                    error="No response (timeout)"
                )

        except Exception as e:
            return PingCheckTaskResult(
                success=False,
                error=str(e)
            )


class PingCheckTaskResult(BaseCheckTaskResult):
    type: Literal[CheckTaskTypeEnum.PING] = CheckTaskTypeEnum.PING
    response_time: float | None = None  # seconds
    success: bool = False
    error: str | None = None
