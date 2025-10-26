import validators
from pydantic import BaseModel, IPvAnyAddress
from aiodns import DNSResolver
from urllib.parse import urlparse


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


def flexible_parse(uri: str):
    if "://" not in uri:
        uri = "http://" + uri
    return urlparse(uri)


async def resolve_endpoint(endpoint: str) -> ResolvedEndpoint:
    uri = flexible_parse(endpoint)

    ipv4 = []
    ipv6 = []
    domain = None

    if validators.ipv4(uri.netloc):
        ipv4.append(uri.netloc)
    elif validators.ipv6(uri.netloc):
        ipv6.append(uri.netloc)
    else:
        domain = uri.netloc
        resolver = DNSResolver()
        ipv4.extend(map(str,
            await resolver.query(domain, "A")
        ))
        ipv6.extend(map(str,
            await resolver.query(domain, "AAAA")
        ))

    return ResolvedEndpoint.model_validate(dict(
        domain=domain,
        ipv4=ipv4,
        ipv6=ipv6,
    ))
