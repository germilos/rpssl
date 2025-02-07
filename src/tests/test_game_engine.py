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
def test_play_single_player_anonymous(
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
