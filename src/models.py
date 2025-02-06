from src.enums import Choice


class Game:
    def __init__(
        self,
        first_player: str,
        second_player: str,
        first_player_choice: Choice,
        second_player_choice: Choice,
        winner: str,
    ):
        self.first_player = first_player
        self.second_player = second_player
        self.first_player_choice = first_player_choice
        self.second_player_choice = second_player_choice
        self.winner = winner
