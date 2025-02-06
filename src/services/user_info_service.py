from typing import Dict

from src.services.leaderboard_service import LeaderboardService
from src.storage.user_info_storage import UserGameInfoStorage


class UserGameInfoService:
    def __init__(self, user_game_info_storage: UserGameInfoStorage, leaderboard_service: LeaderboardService):
        self.leaderboard_service = leaderboard_service
        self.user_game_info_storage = user_game_info_storage

    def add_game(self, game: Dict):
        winner = game["winner"]
        loser = game["first_player"] if game["first_player"] != game["winner"] else game["second_player"]

        winner_info = self.user_game_info_storage.add_user_win(winner, game)
        self.user_game_info_storage.add_user_loss(loser, game)

        self.leaderboard_service.add_user_score(winner, winner_info["wins"])
