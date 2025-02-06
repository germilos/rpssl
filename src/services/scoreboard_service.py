from typing import Dict, List

from src.singleton import Singleton
from src.storage.scoreboard_storage import ScoreboardStorage


class ScoreboardService(metaclass=Singleton):
    def __init__(self, scoreboard_storage: ScoreboardStorage):
        self.scoreboard_storage = scoreboard_storage

    def add_game_score(self, game: Dict):
        self.scoreboard_storage.add(game)

    def reset_game_scores(self):
        self.scoreboard_storage.clear()

    def get_scoreboard(self) -> List[Dict]:
        return self.scoreboard_storage.get_all()
