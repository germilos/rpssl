from starlette.testclient import TestClient
from starlette import status
from src.enums import choices, Choice


def test_health(client: TestClient):
    url = "/api/v1/health"
    resp = client.get(url=url)

    assert resp.status_code == status.HTTP_200_OK


def test_get_choices(client: TestClient):
    url = "/api/v1/choices"
    resp = client.get(url=url)

    assert resp.status_code == status.HTTP_200_OK
    resp_payload = resp.json()
    assert len(resp_payload) == len(choices)


def test_get_random_choice(client: TestClient):
    url = "/api/v1/choice"
    resp = client.get(url=url)

    assert resp.status_code == status.HTTP_200_OK
    resp_payload = resp.json()

    values = set(choice.value for choice in Choice)

    assert resp_payload["id"] in choices.keys()
    assert resp_payload["name"] in values
