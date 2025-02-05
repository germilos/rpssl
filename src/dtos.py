from typing import Optional

from pydantic import field_validator, BaseModel

from src.enums import choices
from src.exceptions import APIError, InvalidChoice


class ChoiceRequestDto(BaseModel):
    choice: int

    @field_validator("choice")
    def validate_choice(cls, v: Optional[int]) -> int:
        if v not in choices.keys():
            raise APIError(error=InvalidChoice())
        return v
