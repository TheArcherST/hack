from __future__ import annotations

import asyncio
from typing import Any, Optional, Literal

from pydantic import IPvAnyAddress, Field

from .base import BaseCheckTaskPayload, BaseCheckTaskResult
from .type_enum import CheckTaskTypeEnum


class TCPUDPCheckTaskPayload(BaseCheckTaskPayload):
    type: Literal[CheckTaskTypeEnum.TCP_AND_UDP] = CheckTaskTypeEnum.TCP_AND_UDP
    ip: IPvAnyAddress
    port: int = Field(..., ge=1, le=65535)
    protocol: str = Field("tcp", pattern="^(tcp|udp)$")
    timeout: int = 5

    async def perform_check(self) -> TCPUDPCheckTaskResult:
        if self.protocol.lower() == "tcp":
            result = await self._check_tcp()
        else:
            result = await self._check_udp()

        if "error" in result:
            return TCPUDPCheckTaskResult(error=result["error"])

        return TCPUDPCheckTaskResult(**result)

    async def _check_tcp(self) -> dict[str, Any]:
        async def run_check():
            start = asyncio.get_event_loop().time()
            try:
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(str(self.ip), self.port),
                    timeout=self.timeout,
                )
                writer.close()
                await writer.wait_closed()
                elapsed = (asyncio.get_event_loop().time() - start) * 1000
                return {
                    "reachable": True,
                    "latency_ms": round(elapsed, 2),
                    "protocol": "tcp",
                    "port": self.port,
                    "ip": str(self.ip),
                }
            except Exception as e:
                return {"error": str(e)}

        return await run_check()

    async def _check_udp(self) -> dict[str, Any]:
        async def run_check():
            start = asyncio.get_event_loop().time()
            try:
                loop = asyncio.get_event_loop()
                on_response = loop.create_future()

                transport, _ = await loop.create_datagram_endpoint(
                    asyncio.DatagramProtocol,
                    remote_addr=(str(self.ip), self.port),
                )

                transport.sendto(b"ping")

                try:
                    await asyncio.wait_for(on_response, timeout=self.timeout)
                except asyncio.TimeoutError:
                    # UDP often gives no response — consider open if no error
                    pass

                elapsed = (asyncio.get_event_loop().time() - start) * 1000
                transport.close()

                return {
                    "reachable": True,
                    "latency_ms": round(elapsed, 2),
                    "protocol": "udp",
                    "port": self.port,
                    "ip": str(self.ip),
                }
            except Exception as e:
                return {"error": str(e)}

        return await run_check()


class TCPUDPCheckTaskResult(BaseCheckTaskResult):
    type: Literal[CheckTaskTypeEnum.TCP_AND_UDP] = CheckTaskTypeEnum.TCP_AND_UDP
    reachable: bool | None = None
    latency_ms: float | None = None
    protocol: str | None = None
    port: int | None = None
    ip: str | None = None
    error: Optional[str] = None
