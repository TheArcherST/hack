from __future__ import annotations

import asyncio
from typing import Any, Optional, Literal

import geoip2.database
from pydantic import IPvAnyAddress, Field
from scapy.all import sr1, IP, ICMP

from .base import BaseCheckTaskPayload, BaseCheckTaskResult
from .type_enum import CheckTaskTypeEnum


class TracerouteCheckTaskPayload(BaseCheckTaskPayload):
    type: Literal[CheckTaskTypeEnum.TRACEROUTE] = CheckTaskTypeEnum.TRACEROUTE
    ip: IPvAnyAddress
    max_ttl: int = Field(30, ge=1, le=255)
    timeout: int = 2
    db_path: str = "/usr/src/app/GeoLite2-City.mmdb"

    async def perform_check(self) -> TracerouteCheckTaskResult:
        reader = geoip2.database.Reader(self.db_path)
        def run_trace() -> dict[str, Any]:
            hops: list[dict[str, Any]] = []

            for ttl in range(1, self.max_ttl + 1):
                pkt = IP(dst=str(self.ip), ttl=ttl) / ICMP()
                reply = sr1(pkt, verbose=0, timeout=self.timeout)

                hop_info: dict[str, Any] = {"ttl": ttl}
                if reply is None:
                    hop_info["host"] = None
                    hop_info["status"] = "timeout"
                else:
                    hop_info["host"] = reply.src
                    hop_info["status"] = "ok"
                    hops.append(hop_info)

                    if reply.src == str(self.ip):
                        break

                hops.append((hop_info, reader.city(reply.src).country))

            # If no hops were recorded, likely unreachable
            if not hops:
                return {"error": "No ICMP response received"}

            return {"hops": hops, "target": str(self.ip)}

        data = await asyncio.to_thread(run_trace)

        if "error" in data:
            return TracerouteCheckTaskResult(error=data["error"])

        return TracerouteCheckTaskResult(**data)


class TracerouteCheckTaskResult(BaseCheckTaskResult):
    type: Literal[CheckTaskTypeEnum.TRACEROUTE] = CheckTaskTypeEnum.TRACEROUTE
    target: str | None = None
    hops: list[dict[tuple[str, str], Any]] | None = None
    error: Optional[str] = None
