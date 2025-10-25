from deepdiff import DeepDiff
from pydantic import BaseModel

from . import api_templates


def test_streams(
        client,
        authed_client,
):
    req = api_templates.make_issue_agent_create_credentials()
    r = client.prepsend(req)
    assert r.status_code == 201
