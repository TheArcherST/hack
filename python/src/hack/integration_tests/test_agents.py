from deepdiff import DeepDiff
from pydantic import BaseModel

from . import api_templates


def test_streams(
        client,
        authed_client,
):
    req = api_templates.make_create_agent()
    req.json = {
        "port": 52141,
    }
    r = client.prepsend(req)
    assert r.status_code == 201
    assert "52141" in str(r.json())
