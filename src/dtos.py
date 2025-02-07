import uuid
from typing import Optional, Dict

from pydantic import field_validator, BaseModel

from src.enums import choices, Choice, GameResult
from src.exceptions import APIError, InvalidChoice


class ChoiceRequestDto(BaseModel):
    player: int
    username: Optional[str] = None

    @field_validator("player", mode="before")
    def validate_choice(cls, v: Optional[int]) -> int:
        if isinstance(v, int) and v in choices.keys():
            return v
        raise APIError(error=InvalidChoice())


class CreateGameRequestDto(BaseModel):
    username: str
    choice: int


class PlayGameRequestDto(BaseModel):
    username: str
    choice: int
    game_id: Optional[uuid.UUID] = None

    @field_validator("choice")
    def validate_choice(cls, v: Optional[int]) -> int:
        if v not in choices.keys():
            raise APIError(error=InvalidChoice())
        return v


class ChoiceDto(BaseModel):
    id: int
    name: Choice


class SinglePlayerResultDto(BaseModel):
    results: GameResult
    player: int
    computer: int


class MultiPlayerResultDto(BaseModel):
    results: GameResult
    first_player: str
    first_player_choice: int
    second_player: str
    second_player_choice: int


class GameDto(BaseModel):
    game_id: uuid.UUID
    first_player: str
    first_player_choice: int
    second_player: Optional[str] = None
    second_player_choice: Optional[int] = None
    winner: Optional[str] = None

    @staticmethod
    def from_dict(dict_values: Dict) -> "GameDto":
        return GameDto(
            game_id=dict_values["game_id"],
            first_player=dict_values["first_player"],
            first_player_choice=dict_values["first_player_choice"],
            second_player=dict_values["second_player"]
            if dict_values["second_player"] is not None
            else None,
            second_player_choice=dict_values["second_player_choice"]
            if dict_values["second_player_choice"] is not None
            else None,
            winner=dict_values["winner"] if dict_values["winner"] is not None else None,
        )


class SkinnyGameDto(BaseModel):
    game_id: uuid.UUID
    first_player: str
    second_player: Optional[str] = None
    winner: Optional[str] = None

    @staticmethod
    def from_dict(dict_values: Dict) -> "SkinnyGameDto":
        return SkinnyGameDto(
            game_id=dict_values["game_id"],
            first_player=dict_values["first_player"],
            second_player=dict_values["second_player"]
            if dict_values["second_player"] is not None
            else None,
            winner=dict_values["winner"] if dict_values["winner"] is not None else None,
        )


class UserScoreDto(BaseModel):
    user: str
    score: int
