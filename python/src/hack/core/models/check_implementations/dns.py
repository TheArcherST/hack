from __future__ import annotations

import asyncio
from typing import Literal

from aiodns import DNSResolver

from .base import BaseCheckTaskPayload, BaseCheckTaskResult
from .commands import flexible_parse
from .type_enum import CheckTaskTypeEnum


class DNSCheckTaskPayload(BaseCheckTaskPayload):
    type: Literal[CheckTaskTypeEnum.DNS] = CheckTaskTypeEnum.DNS
    url: str

    async def perform_check(self) -> DNSCheckTaskResult:
        domain = flexible_parse(self.url).netloc

        resolver = DNSResolver()

        # Run all lookups concurrently
        a_task = resolver.query(domain, "A")
        aaaa_task = resolver.query(domain, "AAAA")
        mx_task = resolver.query(domain, "MX")
        ns_task = resolver.query(domain, "NS")
        txt_task = resolver.query(domain, "TXT")
        cname_task = resolver.query(domain, "CNAME")

        # Wait for all tasks
        a_records, aaaa_records, mx_records, ns_records, txt_records, cname_records = await asyncio.gather(
            a_task, aaaa_task, mx_task, ns_task, txt_task, cname_task
        )

        return DNSCheckTaskResult.model_validate(dict(
            a_records=a_records,
            aaaa_records=aaaa_records,
            mx_records=mx_records,
            ns_records=ns_records,
            txt_records=txt_records,
            cname_records=cname_records,
        ))


class DNSCheckTaskResult(BaseCheckTaskResult):
    type: Literal[CheckTaskTypeEnum.DNS] = CheckTaskTypeEnum.DNS

    a_records: list[str] | None = None
    aaaa_records: list[str] | None = None
    mx_records: list[str] | None = None
    ns_records: list[str] | None = None
    cname_records: list[str] | None = None
    txt_records: list[str] | None = None
