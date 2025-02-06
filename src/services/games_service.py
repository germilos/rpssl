import uuid
from typing import List, Dict, Optional

from src import utils
from src.storage.games_storage import GamesStorage


class GamesService:
    def __init__(self, games_storage: GamesStorage):
        self.games_storage = games_storage

    def create_active_game(self, created_by: str, initial_choice: int):
        new_game = {
            "first_player": created_by,
            "first_player_choice": initial_choice,
            "second_player": None,
            "second_player_choice": None,
            "winner": None,
        }
        return self.games_storage.create_active_game(new_game)

    def get_active_games(self) -> List[Dict]:
        return self.games_storage.get_active_games()

    def get_active_game_by_id(self, game_id: uuid.UUID) -> Optional[Dict]:
        return self.games_storage.get_active_game_by_id(game_id)

    def get_random_active_game(self) -> Dict:
        random_number = utils.generate_random_choice_id()
        active_games = self.get_active_games()
        random_game = active_games[random_number % len(active_games)]
        return random_game

    def get_completed_games(self) -> List[Dict]:
        return self.games_storage.get_completed_games()

    def complete_game(self, game_id: uuid.UUID) -> uuid.UUID:
        active_game = self.games_storage.get_active_game_by_id(game_id)
        self.games_storage.add_completed_game(active_game)
        self.games_storage.remove_active_game(game_id)

        return game_id
