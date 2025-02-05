from enum import Enum


class Choice(str, Enum):
    ROCK = "Rock"
    PAPER = "Paper"
    SCISSORS = "Scissors"
    LIZARD = "Lizard"
    SPOCK = "Spock"


choices = {
    1: Choice.ROCK,
    2: Choice.PAPER,
    3: Choice.SCISSORS,
    4: Choice.LIZARD,
    5: Choice.SPOCK,
}
