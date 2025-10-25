from typing import Annotated

from pydantic import Discriminator, TypeAdapter

from .dns import DNSCheckTaskPayload, DNSCheckTaskResult
from .nmap import Nmap3CheckTaskPayload, Nmap3CheckTaskResult
from .http import HTTPCheckTaskPayload, HTTPCheckTaskResult
from .geoip import GeoIPCheckTaskPayload, GeoIPCheckTaskResult
from .tcp_and_udp import TCPUDPCheckTaskPayload, TCPUDPCheckTaskResult


type AnyCheckTaskPayloadType = Annotated[
    (
        DNSCheckTaskPayload
        | Nmap3CheckTaskPayload
        | HTTPCheckTaskPayload
        | GeoIPCheckTaskPayload
        | TCPUDPCheckTaskPayload
    ),
    Discriminator("type")
]
AnyCheckTaskPayload = TypeAdapter(AnyCheckTaskPayloadType)

type AnyCheckTaskResultType = Annotated[
    (
        DNSCheckTaskResult
        | Nmap3CheckTaskResult
        | HTTPCheckTaskResult
        | GeoIPCheckTaskResult
        | TCPUDPCheckTaskResult
    ),
    Discriminator("type")
]
AnyCheckTaskResult = TypeAdapter(AnyCheckTaskResultType)
