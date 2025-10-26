from __future__ import annotations

import asyncio
import nmap3
from pydantic import IPvAnyAddress, HttpUrl
from typing import Any, Literal

from hack.core.models.check_implementations.base import BaseCheckTaskPayload, BaseCheckTaskResult
from hack.core.models.check_implementations.commands import resolve_endpoint
from hack.core.models.check_implementations.type_enum import CheckTaskTypeEnum


class Nmap3CheckTaskPayload(BaseCheckTaskPayload):
    type: Literal[CheckTaskTypeEnum.NMAP] = CheckTaskTypeEnum.NMAP
    url: str
    ports: str | None = None  # optional (for future use)

    async def perform_check(self) -> Nmap3CheckTaskResult:
        """
        Perform asynchronous Nmap3 checks:
        - Version detection
        - OS detection
        - Top port scan
        """
        self.url = (await resolve_endpoint(self.url)).domain
        nmap = nmap3.Nmap()

        async def run_version_detection() -> dict[str, Any]:
            return await asyncio.to_thread(nmap.nmap_version_detection, str(self.url))

        async def run_os_detection() -> dict[str, Any]:
            return await asyncio.to_thread(nmap.nmap_os_detection, str(self.url))

        async def run_top_ports() -> dict[str, Any]:
            return await asyncio.to_thread(nmap.scan_top_ports, str(self.url))

        try:
            # Run all scans concurrently
            version_task = asyncio.create_task(run_version_detection())
            os_task = asyncio.create_task(run_os_detection())
            ports_task = asyncio.create_task(run_top_ports())

            version_detection, os_detection, top_ports = await asyncio.gather(
                version_task, os_task, ports_task
            )

            return Nmap3CheckTaskResult(
                version_detection=version_detection,
                os_detection=os_detection,
                top_ports=top_ports,
            )

        except Exception as e:
            return Nmap3CheckTaskResult(error=str(e))


class Nmap3CheckTaskResult(BaseCheckTaskResult):
    type: Literal[CheckTaskTypeEnum.NMAP] = CheckTaskTypeEnum.NMAP

    os_detection: dict[str, Any] | None = None
    version_detection: dict[str, Any] | None = None
    top_ports: dict[str, Any] | None = None
    error: str | None = None