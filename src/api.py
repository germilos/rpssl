from typing import Dict, List, Optional

from fastapi import APIRouter, Depends
from starlette import status

from src import utils
from src.dtos import ChoiceRequestDto, CreateGameRequestDto, PlayGameRequestDto

from src.enums import choices
from src.resolvers import (
    get_leaderboard_service,
    get_games_service,
    get_recent_games_service,
    get_game_engine,
)
from src.services.games_service import GamesService
from src.services.leaderboard_service import (
    LeaderboardService,
)
from src.services.scoreboard_service import RecentGamesService

router = APIRouter()


@router.get("/health", status_code=status.HTTP_200_OK)
def get_health() -> str:
    return "OK"


@router.get("/choices", status_code=status.HTTP_200_OK)
def get_choices() -> List[Dict]:
    return [{"id": choice, "name": name} for choice, name in choices.items()]


@router.get("/choice", status_code=status.HTTP_200_OK)
def get_random_choice() -> Dict:
    test = utils.generate_random_choice_id()
    return {"id": test, "name": choices[test]}


@router.post("/play", status_code=status.HTTP_200_OK)
def play(request_dto: ChoiceRequestDto, game_engine=Depends(get_game_engine)) -> Dict:
    return game_engine.single_player(request_dto.choice, request_dto.username)


@router.post("/multiplayer", status_code=status.HTTP_200_OK)
def play_multiplayer(
    request_dto: PlayGameRequestDto, game_engine=Depends(get_game_engine)
):
    return game_engine.multiplayer(
        request_dto.username, request_dto.choice, request_dto.game_id
    )


@router.get("/scoreboard", status_code=status.HTTP_200_OK)
def scoreboard(
    recent_games_service: RecentGamesService = Depends(get_recent_games_service),
) -> List:
    return recent_games_service.get_recent_games()


@router.delete("/scoreboard", status_code=status.HTTP_200_OK)
def reset_scoreboard(
    recent_games_service: RecentGamesService = Depends(get_recent_games_service),
):
    recent_games_service.reset_recent_games()


@router.get("/leaderboard", status_code=status.HTTP_200_OK)
def get_leaderboard(
    leaderboard_service: LeaderboardService = Depends(get_leaderboard_service),
):
    return leaderboard_service.get_top_players()


@router.post("/games", status_code=status.HTTP_200_OK)
def create_game(
    request_dto: CreateGameRequestDto,
    games_service: GamesService = Depends(get_games_service),
):
    return games_service.create_active_game(request_dto.username, request_dto.choice)


@router.get("/games", status_code=status.HTTP_200_OK)
def get_games(
    active: Optional[bool] = True,
    games_service: GamesService = Depends(get_games_service),
):
    if active:
        return games_service.get_active_games()
    else:
        return games_service.get_completed_games()
