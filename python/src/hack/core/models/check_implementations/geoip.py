from __future__ import annotations

import geoip2.database
from pydantic import AnyUrl, BaseModel
from typing import Literal

from .base import BaseCheckTaskPayload, BaseCheckTaskResult
from .commands import resolve_endpoint
from .type_enum import CheckTaskTypeEnum


class GeoIPCheckTaskPayload(BaseCheckTaskPayload):
    type: Literal[CheckTaskTypeEnum.GEOIP] = CheckTaskTypeEnum.GEOIP
    url: AnyUrl
    db_asn_path: str = "/usr/src/app/GeoLite2-ASN.mmdb"
    db_path: str = "/usr/src/app/GeoLite2-City.mmdb"

    async def perform_check(self) -> GeoIPCheckTaskResult:
        resolved_endpoint = await resolve_endpoint(self.url)
        items = []
        with (
            geoip2.database.Reader(self.db_asn_path) as asn_reader,
            geoip2.database.Reader(self.db_path) as reader
        ):
            for ip in resolved_endpoint.ipv4:
                asn_response = asn_reader.asn(str(ip))
                response = reader.city(str(ip))
                items.append(GeoIPItem(
                    country=response.country.name,
                    city=response.city.name,
                    region=response.subdivisions.most_specific.name,
                    postal_code=response.postal.code,
                    latitude=response.location.latitude,
                    longitude=response.location.longitude,
                    time_zone=response.location.time_zone,
                    organization=asn_response.autonomous_system_organization,
                ))
        return GeoIPCheckTaskResult(
            items=items,
        )


class GeoIPItem(BaseModel):
    country: str | None = None
    city: str | None = None
    region: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    time_zone: str | None = None
    organization: str | None = None
    error: str | None = None
    postal_code: int | None = None


class GeoIPCheckTaskResult(BaseCheckTaskResult):
    type: Literal[CheckTaskTypeEnum.GEOIP] = CheckTaskTypeEnum.GEOIP
    items: list[GeoIPItem]
