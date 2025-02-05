import abc
from uuid import uuid4

from src import utils
from src.enums import Choice, choices

rules = {
    Choice.ROCK: {Choice.LIZARD, Choice.SCISSORS},
    Choice.PAPER: {Choice.ROCK, Choice.SPOCK},
    Choice.SCISSORS: {Choice.PAPER, Choice.LIZARD},
    Choice.LIZARD: {Choice.SPOCK, Choice.PAPER},
    Choice.SPOCK: {Choice.SCISSORS, Choice.ROCK},
}

games = {

}
active_games = {}


class GameEngine(abc.ABC):
    def play(self, choice: Choice):
        raise NotImplementedError


class RPSSLGameEngine(GameEngine):
    def play(self, choice: int):
        computer_choice = utils.fetch_random_number()
        computer_choice_value = choices[computer_choice]
        choice_value = choices[choice]
        choice_beats = rules[choice_value]
        if computer_choice == choice:
            return {"results": "tie", "player": choice, "computer": computer_choice}
        if computer_choice_value in choice_beats:
            return {"results": "win", "player": choice, "computer": computer_choice}
        else:
            return {"results": "loss", "player": choice, "computer": computer_choice}

    def get_active_games(self):
        if len(active_games) == 0:
            return []

        return active_games.keys()

    def play_multiplayer(self, username, choice, game_id=None):
        if game_id is None:
            new_game_id = str(uuid4()),
            new_game = {"first_player": username, "first_player_choice": choice, "second_player": None, "second_player_choice": None}
            active_games[new_game_id] = new_game
            return

        if game_id not in active_games:
            if game_id in games:
                raise Exception("Game already finished!")  # Return game info
            raise Exception("Game doesn't exist!")

        active_game = active_games[game_id]
        active_game["second_player"] = username
        active_game["second_player_choice"] = choice

    def _resolve_winner(self, game):
        raise NotImplementedError


