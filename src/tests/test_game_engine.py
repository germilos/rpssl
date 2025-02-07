import uuid
from typing import Optional

import pytest
from starlette import status
from starlette.testclient import TestClient

from src.enums import GameResult


@pytest.mark.parametrize(
    "computer_choice,player_choice,outcome,username",
    [
        (2, 1, GameResult.LOSS, None),
        (2, 3, GameResult.WIN, "Stephen"),
        (5, 1, GameResult.LOSS, "Stephen"),
        (4, 3, GameResult.WIN, "Stephen"),
        (3, 3, GameResult.TIE, "Stephen"),
    ],
)
def test_play_single_player(
    mocker,
    client: TestClient,
    computer_choice: int,
    player_choice: int,
    outcome: GameResult,
    username: Optional[str],
):
    url = "/api/v1/play"

    random_gen_mock = mocker.patch("src.utils.generate_random_choice_id")
    random_gen_mock.return_value = computer_choice

    mocker.patch("src.services.recent_games_service.RecentGamesService.add_game")
    mocker.patch("src.services.user_game_info_service.UserGameInfoService.add_game")

    payload = dict(player=player_choice, username=username)

    resp = client.post(url=url, json=payload)

    assert resp.status_code == status.HTTP_200_OK
    resp_payload = resp.json()

    assert resp_payload["results"] == outcome.value


@pytest.mark.parametrize(
    "second_player_choice,first_player_choice,outcome,username, game_id",
    [
        (3, 1, GameResult.LOSS, "Stephen", None),
        (2, 1, GameResult.WIN, "Stephen", None),
        (1, 1, GameResult.TIE, "Stephen", None),
        (1, 1, GameResult.TIE, "Stephen", None),
        (
            1,
            1,
            GameResult.TIE,
            "Stephen",
            uuid.UUID("fae50000-a704-2292-e1d5-08dd45266f1a"),
        ),
    ],
)
def test_play_multiplayer_random_game(
    mocker,
    second_player_choice: int,
    first_player_choice: int,
    outcome: GameResult,
    username: str,
    game_id: uuid.UUID,
    client: TestClient,
):
    url = "/api/v1/multiplayer"

    random_gen_mock = mocker.patch("src.utils.generate_random_choice_id")
    random_gen_mock.return_value = 3

    first_test_uuid = uuid.uuid4() if game_id is None else game_id
    second_test_uuid = uuid.uuid4()
    first_game = {
        "first_player": "Peter",
        "first_player_choice": first_player_choice,
        "second_player": None,
        "second_player_choice": None,
        "winner": None,
        "game_id": first_test_uuid if game_id is None else game_id,
    }
    second_game = {
        "first_player": "Tom",
        "first_player_choice": first_player_choice,
        "second_player": None,
        "second_player_choice": None,
        "winner": None,
        "game_id": second_test_uuid,
    }

    get_active_games_mock = mocker.patch(
        "src.storage.games_storage.InMemoryGameStore.get_active_games"
    )
    get_active_games_mock.return_value = {
        first_test_uuid: first_game,
        second_test_uuid: second_game,
    }

    mocker.patch("src.services.recent_games_service.RecentGamesService.add_game")
    mocker.patch("src.services.user_game_info_service.UserGameInfoService.add_game")
    mocker.patch("src.services.games_service.GamesService.complete_game")

    payload = dict(
        choice=second_player_choice,
        username=username,
        game_id=str(game_id) if game_id is not None else None,
    )

    resp = client.post(url=url, json=payload)

    assert resp.status_code == status.HTTP_200_OK
    resp_payload = resp.json()

    assert resp_payload["results"] == outcome
    assert resp_payload[username] == second_player_choice
