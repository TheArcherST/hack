from __future__ import annotations

import asyncio
from typing import Literal

import pydig

from .base import BaseCheckTaskPayload, BaseCheckTaskResult
from .type_enum import CheckTaskTypeEnum


class DNSCheckTaskPayload(BaseCheckTaskPayload):
    type: Literal[CheckTaskTypeEnum.DNS] = CheckTaskTypeEnum.DNS
    domain: str

    async def perform_check(self) -> DNSCheckTaskResult:
        domain = self.domain

        async def query(record_type: str) -> list[str]:
            # Run pydig.query in a thread to avoid blocking
            return await asyncio.to_thread(pydig.query, domain, record_type)

        # Run all lookups concurrently
        a_task = asyncio.create_task(query("A"))
        aaaa_task = asyncio.create_task(query("AAAA"))
        mx_task = asyncio.create_task(query("MX"))
        ns_task = asyncio.create_task(query("NS"))
        txt_task = asyncio.create_task(query("TXT"))
        cname_task = asyncio.create_task(query("CNAME"))

        # Wait for all tasks
        a_records, aaaa_records, mx_records, ns_records, txt_records, cname_records = await asyncio.gather(
            a_task, aaaa_task, mx_task, ns_task, txt_task, cname_task
        )

        return DNSCheckTaskResult(
            a_records=a_records,
            aaaa_records=aaaa_records,
            mx_records=mx_records,
            ns_records=ns_records,
            txt_records=txt_records,
            cname_records=cname_records,
        )


class DNSCheckTaskResult(BaseCheckTaskResult):
    type: Literal[CheckTaskTypeEnum.DNS] = CheckTaskTypeEnum.DNS

    a_records: list[str] | None = None
    aaaa_records: list[str] | None = None
    mx_records: list[str] | None = None
    ns_records: list[str] | None = None
    cname_records: list[str] | None = None
    txt_records: list[str] | None = None
