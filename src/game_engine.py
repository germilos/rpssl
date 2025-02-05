import abc

from src import utils
from src.enums import Choice, choices

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



