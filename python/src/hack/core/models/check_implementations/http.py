from __future__ import annotations

import asyncio
import aiohttp
from typing import Any, Optional, Literal
from pydantic import HttpUrl, IPvAnyAddress

from .base import BaseCheckTaskPayload, BaseCheckTaskResult
from .commands import resolve_endpoint
from .type_enum import CheckTaskTypeEnum


class HTTPCheckTaskPayload(BaseCheckTaskPayload):
    type: Literal[CheckTaskTypeEnum.HTTP] = CheckTaskTypeEnum.HTTP
    url: str
    timeout: int = 10
    verify_ssl: bool = False
    follow_redirects: bool = True
    method: str = "GET"
    headers: dict[str, str] | None = None
    body: Optional[str] = None

    async def perform_check(self) -> HTTPCheckTaskResult:
        resolved_endpoint = await resolve_endpoint(self.url)
        async def check_http() -> dict[str, Any]:
            try:
                timeout = aiohttp.ClientTimeout(total=self.timeout)
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    async with session.request(
                        method=self.method,
                        url=str(resolved_endpoint.domain or resolved_endpoint.some_ip),
                        headers=self.headers,
                        data=self.body,
                        allow_redirects=self.follow_redirects,
                        # ssl=self.verify_ssl,
                    ) as response:
                        content = await response.text(errors="ignore")
                        return {
                            "status_code": response.status,
                            "reason": response.reason,
                            "headers": dict(response.headers),
                            "final_url": str(response.url),
                            "content_snippet": content[:500],  # limit to avoid huge responses
                        }
            except Exception as e:
                return {"error": str(e)}

        data = await asyncio.to_thread(lambda: asyncio.run(check_http()))

        if "error" in data:
            return HTTPCheckTaskResult(error=data["error"])

        return HTTPCheckTaskResult(**data)


class HTTPCheckTaskResult(BaseCheckTaskResult):
    type: Literal[CheckTaskTypeEnum.HTTP] = CheckTaskTypeEnum.HTTP

    status_code: int | None = None
    reason: str | None = None
    headers: dict[str, Any] | None = None
    final_url: str | None = None
    content_snippet: str | None = None
    error: str | None = None
