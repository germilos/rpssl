from typing import Dict, List

from fastapi import APIRouter
from starlette import status

from src import utils
from src.dtos import ChoiceRequestDto
from src.enums import choices
from src.game_engine import RPSSLGameEngine

router = APIRouter()


@router.get("/health", status_code=status.HTTP_200_OK)
def get_health() -> str:
    return "OK"


@router.get("/choices", status_code=status.HTTP_200_OK)
def get_choices() -> List[Dict]:
    return [{"id": choice.key, "name": choice.value} for choice in choices.items()]


@router.get("/choice", status_code=status.HTTP_200_OK)
def get_random_choice() -> Dict:
    test = utils.fetch_random_number()
    return {"id": test, "name": choices[test]}


@router.post("/play", status_code=status.HTTP_200_OK)
def play(request_dto: ChoiceRequestDto) -> Dict:
    game_service = RPSSLGameEngine()
    return game_service.play(request_dto.choice)
