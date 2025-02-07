import collections
import uuid

from starlette import status
from starlette.testclient import TestClient


def test_create_game(
    mocker,
    client: TestClient,
):
    choice = 1
    username = "Peter"
    test_uuid = uuid.uuid4()
    new_game = {
        "first_player": username,
        "first_player_choice": choice,
        "second_player": None,
        "second_player_choice": None,
        "winner": None,
        "game_id": test_uuid,
    }

    url = "/api/v1/games"

    game_store_mock = mocker.patch(
        "src.storage.games_storage.InMemoryGameStore.get_active_games"
    )
    game_store_mock.return_value = {test_uuid: new_game}

    get_uuid_mock = mocker.patch("uuid.uuid4")
    get_uuid_mock.return_value = test_uuid

    payload = dict(choice=choice, username=username)

    resp = client.post(url=url, json=payload)
    resp_payload = resp.json()

    assert resp.status_code == status.HTTP_200_OK

    assert resp_payload["first_player"] == username
    assert resp_payload["first_player_choice"] == choice
    assert resp_payload["game_id"] == str(test_uuid)
    assert resp_payload["second_player"] is None
    assert resp_payload["second_player_choice"] is None


def test_get_active_games(
    mocker,
    client: TestClient,
):
    choice = 1
    first_test_uuid = uuid.uuid4()
    second_test_uuid = uuid.uuid4()
    first_game = {
        "first_player": "Peter",
        "first_player_choice": choice,
        "second_player": None,
        "second_player_choice": None,
        "winner": None,
        "game_id": first_test_uuid,
    }
    second_game = {
        "first_player": "Tom",
        "first_player_choice": choice,
        "second_player": None,
        "second_player_choice": None,
        "winner": None,
        "game_id": second_test_uuid,
    }

    url = "/api/v1/games"

    get_active_games_mock = mocker.patch(
        "src.storage.games_storage.InMemoryGameStore.get_active_games"
    )
    get_active_games_mock.return_value = {
        first_test_uuid: first_game,
        second_test_uuid: second_game,
    }

    get_uuid_mock = mocker.patch("uuid.uuid4")
    get_uuid_mock.side_effect = [first_test_uuid, second_test_uuid]

    resp = client.get(url=url)
    resp_payload = resp.json()

    assert resp.status_code == status.HTTP_200_OK

    assert len(resp_payload) == 2
    assert resp_payload[0]["first_player"] == "Peter"
    assert resp_payload[1]["first_player"] == "Tom"


def test_get_scoreboard(
    mocker,
    client: TestClient,
):
    first_test_uuid = uuid.uuid4()
    second_test_uuid = uuid.uuid4()
    first_game = {
        "first_player": "Peter",
        "first_player_choice": 1,
        "second_player": "Stephen",
        "second_player_choice": 2,
        "winner": "Peter",
        "game_id": first_test_uuid,
    }
    second_game = {
        "first_player": "Tom",
        "first_player_choice": 1,
        "second_player": "Christy",
        "second_player_choice": 3,
        "winner": "Christy",
        "game_id": second_test_uuid,
    }

    recent_games = collections.deque()
    recent_games.append(first_game)
    recent_games.append(second_game)

    url = "/api/v1/scoreboard"

    get_recent_games_mock = mocker.patch(
        "src.storage.recent_games_storage.InMemoryRecentGamesStore.get_games"
    )
    get_recent_games_mock.return_value = recent_games

    resp = client.get(url=url)
    resp_payload = resp.json()

    assert resp.status_code == status.HTTP_200_OK

    assert len(resp_payload) == 2
    assert resp_payload[0]["first_player"] == "Tom"
    assert resp_payload[1]["first_player"] == "Peter"


def test_get_leaderboard(mocker, client: TestClient):
    leaderboard = collections.defaultdict()
    leaderboard["Peter"] = 10
    leaderboard["Tom"] = 5
    leaderboard["Christy"] = 15
    leaderboard["Stephen"] = 11
    leaderboard["Angela"] = 2

    url = "/api/v1/leaderboard"

    get_leaderboard_mock = mocker.patch(
        "src.services.leaderboard_service.InMemoryLeaderboardStore.get_leaderboard"
    )
    get_leaderboard_mock.return_value = leaderboard

    resp = client.get(url=url)
    resp_payload = resp.json()

    assert resp.status_code == status.HTTP_200_OK

    assert len(resp_payload) == 5
    assert resp_payload[0]["name"] == "Christy"
    assert resp_payload[-1]["name"] == "Angela"


def test_get_leaderboard_top_10(mocker, client: TestClient):
    leaderboard = collections.defaultdict()
    leaderboard["Peter"] = 10
    leaderboard["Tom"] = 5
    leaderboard["Christy"] = 15
    leaderboard["Stephen"] = 11
    leaderboard["Angela"] = 2
    leaderboard["Anna"] = 20
    leaderboard["Jeff"] = 1
    leaderboard["Sonia"] = 23
    leaderboard["Lara"] = 5
    leaderboard["Fredrik"] = 18
    leaderboard["Jenis"] = 6
    leaderboard["Denis"] = 34

    url = "/api/v1/leaderboard"

    get_leaderboard_mock = mocker.patch(
        "src.services.leaderboard_service.InMemoryLeaderboardStore.get_leaderboard"
    )
    get_leaderboard_mock.return_value = leaderboard

    resp = client.get(url=url)
    resp_payload = resp.json()

    assert resp.status_code == status.HTTP_200_OK

    assert len(resp_payload) == 10
    assert resp_payload[0]["name"] == "Denis"
    assert resp_payload[-1]["name"] == "Lara"


def test_get_leaderboard_empty(mocker, client: TestClient):
    leaderboard = collections.defaultdict()

    url = "/api/v1/leaderboard"

    get_leaderboard_mock = mocker.patch(
        "src.services.leaderboard_service.InMemoryLeaderboardStore.get_leaderboard"
    )
    get_leaderboard_mock.return_value = leaderboard

    resp = client.get(url=url)
    resp_payload = resp.json()

    assert resp.status_code == status.HTTP_200_OK

    assert len(resp_payload) == 0
