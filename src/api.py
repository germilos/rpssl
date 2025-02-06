from typing import Dict, List

from fastapi import APIRouter
from starlette import status

from src import utils
from src.dtos import ChoiceRequestDto, CreateGameRequestDto, PlayGameRequestDto

from src.choices import choices
from src.game_engine import RPSSLGameEngine
from src.services.leaderboard_service import LeaderboardService, InMemoryLeaderboardService, InMemoryLeaderboardStore
from src.services.scoreboard_service import ScoreboardService
from src.services.user_info_service import UserGameInfoService
from src.storage.scoreboard_storage import ScoreboardStorage

router = APIRouter()


@router.get("/health", status_code=status.HTTP_200_OK)
def get_health() -> str:
    return "OK"


@router.get("/choices", status_code=status.HTTP_200_OK)
def get_choices() -> List[Dict]:
    return [{"id": choice, "name": name} for choice, name in choices.items()]


@router.get("/choice", status_code=status.HTTP_200_OK)
def get_random_choice() -> Dict:
    test = utils.fetch_random_number()
    return {"id": test, "name": choices[test]}


@router.post("/play", status_code=status.HTTP_200_OK)
def play(request_dto: ChoiceRequestDto) -> Dict:
    game_service = RPSSLGameEngine()
    return game_service.play(request_dto.choice, request_dto.username)


@router.post("/play_versus_opponent", status_code=status.HTTP_200_OK)
def play(request_dto: PlayGameRequestDto):
    game_service = RPSSLGameEngine()
    game_service.play_multiplayer(request_dto.username, request_dto.choice, request_dto.game_id)

@router.get("/scoreboard", status_code=status.HTTP_200_OK)
def scoreboard() -> List:
    scoreboard = ScoreboardService(ScoreboardStorage())
    return scoreboard.get_scoreboard()


@router.get("/reset_scoreboard", status_code=status.HTTP_200_OK)
def reset_scoreboard():
    scoreboard = ScoreboardService(ScoreboardStorage())
    scoreboard.reset_game_scores()

@router.post("/create_game", status_code=status.HTTP_200_OK)
def create_game(request_dto: CreateGameRequestDto):
    game_engine = RPSSLGameEngine()
    return game_engine.start_new_game(request_dto.username, request_dto.choice)

@router.get("/active_games", status_code=status.HTTP_200_OK)
def get_active_games():
    game_engine = RPSSLGameEngine()
    return game_engine.get_active_games()


@router.get("/leaderboard", status_code=status.HTTP_200_OK)
def get_leaderboard():
    s = InMemoryLeaderboardService(InMemoryLeaderboardStore())
    return s.get_top_players()
