import uuid
from typing import Optional

from pydantic import field_validator, BaseModel

from src.enums import choices
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
