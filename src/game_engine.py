import abc
from typing import Optional

from src import utils
from src.choices import Choice, choices
from src.services.games_service import GamesService
from src.services.leaderboard_service import InMemoryLeaderboardService, InMemoryLeaderboardStore
from src.services.scoreboard_service import ScoreboardService
from src.services.user_info_service import UserGameInfoService
from src.storage.games_storage import InMemoryGamesStorage, InMemoryGameStore
from src.storage.scoreboard_storage import InMemoryScoreboardStorage, InMemoryScoreboardStore
from src.storage.user_info_storage import InMemoryUserGameInfoStorage, InMemoryUserGameInfoStore

rules = {
    Choice.ROCK: {Choice.LIZARD, Choice.SCISSORS},
    Choice.PAPER: {Choice.ROCK, Choice.SPOCK},
    Choice.SCISSORS: {Choice.PAPER, Choice.LIZARD},
    Choice.LIZARD: {Choice.SPOCK, Choice.PAPER},
    Choice.SPOCK: {Choice.SCISSORS, Choice.ROCK},
}


class GameEngine(abc.ABC):
    def play(self, choice: Choice):
        raise NotImplementedError


class RPSSLGameEngine(GameEngine):
    def __init__(self):
        self.rules = {
            Choice.ROCK: {Choice.LIZARD, Choice.SCISSORS},
            Choice.PAPER: {Choice.ROCK, Choice.SPOCK},
            Choice.SCISSORS: {Choice.PAPER, Choice.LIZARD},
            Choice.LIZARD: {Choice.SPOCK, Choice.PAPER},
            Choice.SPOCK: {Choice.SCISSORS, Choice.ROCK},
        }

    def play(self, choice: int, username: Optional[str]=None):
        scoreboard = ScoreboardService(InMemoryScoreboardStorage(InMemoryScoreboardStore()))

        computer_choice = utils.fetch_random_number()
        computer_choice_value = choices[computer_choice]
        choice_value = choices[choice]
        choice_beats = rules[choice_value]
        if computer_choice == choice:
            ret_res = "tie"
            result = {
                "first_player": username if username is not None else "Anonymous",
                "first_player_choice": choice,
                "second_player": "Computer",
                "second_player_choice": computer_choice,
                "winner": "Tie"
            }
        elif computer_choice_value in choice_beats:
            ret_res = "win"
            result = {
                "first_player": username if username is not None else "Anonymous",
                "first_player_choice": choice,
                "second_player": "Computer",
                "second_player_choice": computer_choice,
                "winner": username if username is not None else "Anonymous"
            }
        else:
            ret_res = "loss"
            result = {
                "first_player": username if username is not None else "Anonymous",
                "first_player_choice": choice,
                "second_player": "Computer",
                "second_player_choice": computer_choice,
                "winner": "Computer"
            }
        scoreboard.add_game_score(result)
        return {"results": ret_res, "player": choice, "computer": computer_choice}

    def get_active_games(self):
        game_service = GamesService(InMemoryGamesStorage(InMemoryGameStore()))
        return game_service.get_active_games()

    def start_new_game(self, username, choice):
        games_service = GamesService(InMemoryGamesStorage(InMemoryGameStore()))
        game_id = games_service.create_active_game(username, choice)
        return game_id

    def play_multiplayer(self, username, choice, game_id=None):
        games_service = GamesService(InMemoryGamesStorage(InMemoryGameStore()))
        scoreboard = ScoreboardService(InMemoryScoreboardStorage(InMemoryScoreboardStore()))
        user_scores_service = UserGameInfoService(user_game_info_storage=InMemoryUserGameInfoStorage(InMemoryUserGameInfoStore())
                                                  , leaderboard_service=InMemoryLeaderboardService(InMemoryLeaderboardStore()))
        if game_id is None:
            random_game = games_service.get_random_active_game()

            print(random_game)
            random_game["second_player"] = username
            random_game["second_player_choice"] = choice

            choice_value = choices[random_game["first_player_choice"]]
            choice_beats = rules[choice_value]
            if random_game["second_player_choice"] == random_game["first_player_choice"]:
                random_game["winner"] = "Tie"
            elif random_game["second_player_choice"] in choice_beats:
                random_game["winner"] = random_game["first_player"]
            else:
                random_game["winner"] = random_game["second_player"]
            scoreboard.add_game_score(random_game)
            user_scores_service.add_game(random_game)
            games_service.complete_game(random_game["id"])
            return random_game

        # if game_id not in active_games:
        #     if game_id in games:
        #         raise Exception("Game already finished!")  # Return game info
        #     raise Exception("Game doesn't exist!")

        # active_game = active_games[game_id]
        # active_game["second_player"] = username
        # active_game["second_player_choice"] = choice

    def _resolve_winner(self, game):
        raise NotImplementedError


