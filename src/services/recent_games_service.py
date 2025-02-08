from typing import Dict, List

from src.dtos import GameDto
from src.singleton import Singleton
from src.storage.recent_games_storage import RecentGamesStorage


class RecentGamesService(metaclass=Singleton):
    def __init__(self, recent_games_storage: RecentGamesStorage):
        self.recent_games_storage = recent_games_storage

    def add_game(self, game: Dict):
        self.recent_games_storage.add(game)

    def add_games(self, game: List[Dict]):
        self.recent_games_storage.add_all(game)

    def reset_recent_games(self):
        self.recent_games_storage.clear()

    def get_recent_games(self) -> List[GameDto]:
        return [
            GameDto.from_dict(game_dict)
            for game_dict in self.recent_games_storage.get_all()
        ]
