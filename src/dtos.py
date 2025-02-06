import uuid
from typing import Optional

from pydantic import field_validator, BaseModel

from src.enums import choices
from src.exceptions import APIError, InvalidChoice


class ChoiceRequestDto(BaseModel):
    choice: int
    username: Optional[str] = None

    @field_validator("choice")
    def validate_choice(cls, v: Optional[int]) -> int:
        if v not in choices.keys():
            raise APIError(error=InvalidChoice())
        return v


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


class UserScore:
    def __init__(self, user, score):
        self.user = user
        self.score = score

    def __lt__(self, other):  # To override > operator
        return self.score < other.score
