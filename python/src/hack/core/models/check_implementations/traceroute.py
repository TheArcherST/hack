from __future__ import annotations

import asyncio
import socket
import time
from typing import Literal, Optional, List

import geoip2.database
from geoip2.errors import AddressNotFoundError
from pydantic import BaseModel

from hack.core.models.check_implementations.base import BaseCheckTaskPayload, BaseCheckTaskResult
from hack.core.models.check_implementations.commands import resolve_endpoint
from hack.core.models.check_implementations.type_enum import CheckTaskTypeEnum


class TracerouteHop(BaseModel):
    ttl: int
    ip: str | None = None
    rtt_ms: Optional[float] = None
    city: str | None = None


class TracerouteCheckTaskPayload(BaseCheckTaskPayload):
    type: Literal[CheckTaskTypeEnum.TRACEROUTE] = CheckTaskTypeEnum.TRACEROUTE
    url: str
    max_hops: int = 30
    timeout: int = 2
    db_path: str = "/usr/src/app/GeoLite2-City.mmdb"

    async def perform_check(self) -> TracerouteCheckTaskResult:
        """Perform an asynchronous traceroute."""
        self.url = (await resolve_endpoint(self.url)).domain
        dest_addr = socket.gethostbyname(self.url)
        hops: List[TracerouteHop] = []

        async def trace_hop(ttl: int) -> TracerouteHop:
            recv_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            recv_sock.settimeout(self.timeout)
            send_sock.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

            recv_sock.bind(("", 33434))
            send_sock.sendto(b"", (self.url, 33434))
            start_time = time.time()

            ip = None
            rtt_ms: Optional[float] = None

            try:
                _, curr_addr = recv_sock.recvfrom(512)
                elapsed = (time.time() - start_time) * 1000
                ip = curr_addr[0]
                rtt_ms = round(elapsed, 2)
            except socket.timeout:
                pass
            finally:
                recv_sock.close()
                send_sock.close()

            return TracerouteHop(ttl=ttl, ip=ip, rtt_ms=rtt_ms)

        with geoip2.database.Reader(self.db_path) as reader:
            for ttl in range(1, self.max_hops + 1):
                hop = await trace_hop(ttl)
                if hop.ip:
                    try:
                        city=reader.city(hop.ip).city.name
                    except AddressNotFoundError:
                        city=None
                hops.append(dict(
                    ttl=hop.ttl,
                    ip=hop.ip,
                    rtt_ms=hop.rtt_ms,
                    city=city
                ))
                if hop.ip == dest_addr:
                    break

        return TracerouteCheckTaskResult(
            destination=self.url,
            destination_ip=dest_addr,
            hops=hops,
        )


class TracerouteCheckTaskResult(BaseCheckTaskResult):
    type: Literal[CheckTaskTypeEnum.TRACEROUTE] = CheckTaskTypeEnum.TRACEROUTE

    destination: str
    destination_ip: str
    hops: List[TracerouteHop]