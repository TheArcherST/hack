import validators
from pydantic import AnyUrl, BaseModel, IPvAnyAddress, TypeAdapter
from aiodns import DNSResolver


class ResolvedEndpoint(BaseModel):
    domain: str | None
    ipv4: list[IPvAnyAddress]
    ipv6: list[IPvAnyAddress]

    @property
    def some_ip(self) -> IPvAnyAddress | None:
        if self.ipv4:
            return self.ipv4[0]
        elif self.ipv6:
            return self.ipv6[0]
        else:
            return None


async def resolve_endpoint(endpoint: AnyUrl) -> ResolvedEndpoint:
    ipv4 = []
    ipv6 = []
    domain = None

    if validators.ipv4(endpoint.host):
        ipv4.append(endpoint.host)
    elif validators.ipv6(endpoint.host):
        ipv6.append(endpoint.host)
    else:
        domain = endpoint.host
        resolver = DNSResolver()
        ipv4.extend(
            await resolver.query(domain, "A")
        )
        ipv6.extend(
            await resolver.query(domain, "AAAA")
        )

    return ResolvedEndpoint(
        domain=domain,
        ipv4=ipv4,
        ipv6=ipv6,
    )
