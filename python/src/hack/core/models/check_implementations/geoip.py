from __future__ import annotations

import asyncio
import geoip2.database
from pydantic import IPvAnyAddress
from typing import Any, Literal

from .base import BaseCheckTaskPayload, BaseCheckTaskResult
from .type_enum import CheckTaskTypeEnum


class GeoIPCheckTaskPayload(BaseCheckTaskPayload):
    type: Literal[CheckTaskTypeEnum.GEOIP] = CheckTaskTypeEnum.GEOIP

    ip: IPvAnyAddress
    db_asn_path: str = "/usr/src/app/GeoLite2-ASN.mmdb"
    db_path: str = "/usr/src/app/GeoLite2-City.mmdb"

    async def perform_check(self) -> GeoIPCheckTaskResult:
        async def lookup_ip() -> dict[str, Any]:
            try:
                with geoip2.database.Reader(self.db_asn_path) as asn_reader:
                    with geoip2.database.Reader(self.db_path) as reader:
                        asn_response = asn_reader.asn(str(self.ip))
                        response = reader.city(str(self.ip))
                        return {
                            "country": response.country.name,
                            "city": response.city.name,
                            "region": response.subdivisions.most_specific.name,
                            "postal_code": response.postal.code,
                            "latitude": response.location.latitude,
                            "longitude": response.location.longitude,
                            "time_zone": response.location.time_zone,
                            "organization": asn_response.autonomous_system_organization,
                        }
            except Exception as e:
                return {"error": str(e)}

        data = await asyncio.to_thread(lookup_ip)

        if "error" in data:
            return GeoIPCheckTaskResult(error=data["error"])

        return GeoIPCheckTaskResult(**data)


class GeoIPCheckTaskResult(BaseCheckTaskResult):
    type: Literal[CheckTaskTypeEnum.GEOIP] = CheckTaskTypeEnum.GEOIP

    country: str | None = None
    city: str | None = None
    region: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    time_zone: str | None = None
    organization: str | None = None
    error: str | None = None