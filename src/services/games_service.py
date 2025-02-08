import uuid
from typing import List, Dict, Optional

from src import utils
from src.dtos import GameDto, SkinnyGameDto
from src.enums import choices
from src.storage.games_storage import GamesStorage


class GamesService:
    def __init__(self, games_storage: GamesStorage):
        self.games_storage = games_storage

    def create_active_game(self, created_by: str, initial_choice: int) -> GameDto:
        new_game = {
            "first_player": created_by,
            "first_player_choice": choices[initial_choice],
            "second_player": None,
            "second_player_choice": None,
            "winner": None,
        }
        return GameDto.from_dict(self.games_storage.create_active_game(new_game))

    def get_active_games(self) -> List[Dict]:
        return self.games_storage.get_active_games()

    def get_active_games_skinny(self) -> List[SkinnyGameDto]:
        return [
            SkinnyGameDto.from_dict(game)
            for game in self.games_storage.get_active_games()
        ]

    def get_active_game_by_id(self, game_id: uuid.UUID) -> Optional[Dict]:
        return self.games_storage.get_active_game_by_id(game_id)

    def get_random_active_game(self) -> Optional[Dict]:
        random_number = utils.generate_random_choice_id()
        active_games = self.get_active_games()
        if len(active_games) <= 0:
            return None
        random_game = active_games[random_number % len(active_games)]
        return random_game

    def get_completed_games(self) -> List[Dict]:
        return self.games_storage.get_completed_games()

    def complete_game(self, game_id: uuid.UUID) -> uuid.UUID:
        active_game = self.games_storage.get_active_game_by_id(game_id)
        self.games_storage.add_completed_game(active_game)
        self.games_storage.remove_active_game(game_id)

        return game_id
