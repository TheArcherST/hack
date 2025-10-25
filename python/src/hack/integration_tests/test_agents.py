from deepdiff import DeepDiff
from pydantic import BaseModel

from . import api_templates


def test_streams(
        client,
        authed_client,
):
    req = api_templates.make_create_agent()
    req.json = {
        "name": "Hello world",
        "port": 52141,
        "ip": "147.45.183.24",
    }
    r = client.prepsend(req)
    assert r.status_code == 401
    r = authed_client.prepsend(req)
    assert r.status_code == 201
    assert "52141" in str(r.json())

    req = api_templates.make_get_agents()
    r = authed_client.prepsend(req)
    assert r.status_code == 200

    req = api_templates.make_delete_agent()
    req.path_params = {"agent_id": r.json()[0]["id"]}
    assert r.status_code == 200
