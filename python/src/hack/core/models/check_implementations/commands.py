import asyncio
from ipaddress import IPv4Address, IPv6Address

import pydig
from pydantic import HttpUrl


async def get_ip(url: HttpUrl) -> tuple[IPv4Address, IPv6Address]:


    async def query(record_type: str) -> list[str]:
        # Run pydig.query in a thread to avoid blocking
        return await asyncio.to_thread(pydig.query, url, record_type)

    # Run all lookups concurrently
    a_task = asyncio.create_task(query("A"))
    aaaa_task = asyncio.create_task(query("AAAA"))

    # Wait for all tasks
    a_records, aaaa_records = await asyncio.gather(
        a_task, aaaa_task
    )

    return a_records, aaaa_records

