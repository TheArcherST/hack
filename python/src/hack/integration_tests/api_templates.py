from hack.integration_tests.base import PatchedRequest


_base_url = "http://rest-server"  # docker compose address


def make_create_agent():
    return PatchedRequest(
        method="POST",
        url=_base_url + "/agents",
    )

def make_get_agents():
    return PatchedRequest(
        method="GET",
        url=_base_url + "/agents",
    )

def make_delete_agent():
    return PatchedRequest(
        method="DELETE",
        url=_base_url + "/agents/{agent_id}",
    )

def make_create_stream_proposition():
    return PatchedRequest(
        method="POST",
        url=_base_url + "/streams/{stream_id}/propositions",
    )

def make_get_stream_propositions():
    return PatchedRequest(
        method="GET",
        url=_base_url + "/streams/{stream_id}/propositions",
    )

def make_register():
    return PatchedRequest(
        method="POST",
        url=_base_url + "/register",
    )

def make_login():
    return PatchedRequest(
        method="POST",
        url=_base_url + "/login",
    )
