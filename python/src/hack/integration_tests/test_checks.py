from deepdiff import DeepDiff
from pydantic import BaseModel

from . import api_templates


def test_streams(
        client,
        authed_client,
):
    req = api_templates.make_create_check()
    req.json = {
        "payload": {
            "type": "dns",
            "url": "superlamp.online",
        },
    }
    r = client.prepsend(req)
    assert r.status_code == 201

    req = api_templates.make_create_check()
    req.json = {
        "payload": {
            "type": "geoip",
            "url": "superlamp.online",
        },
    }
    r = client.prepsend(req)
    assert r.status_code == 201

    req = api_templates.make_create_check()
    req.json = {
        "payload": {
            "type": "traceroute",
            "url": "superlamp.online",
        }
    }
    r = client.prepsend(req)
    assert r.status_code == 201

    req = api_templates.make_create_check()
    req.json = {
        "payload": {
            "type": "nmap",
            "url": "superlamp.online",
        }
    }
    r = client.prepsend(req)
    assert r.status_code == 201
