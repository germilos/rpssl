import abc
import logging
import uuid
from typing import Optional

from src import utils
from src.enums import Choice, choices, GameResult, COMPUTER, ANONYMOUS
from src.exceptions import ActiveGameNotFoundError, APIError
from src.services.games_service import GamesService
from src.services.recent_games_service import RecentGamesService
from src.services.user_game_info_service import UserGameInfoService


class GameEngine(abc.ABC):
    def single_player(self, player_choice_id: int, username: Optional[str] = None):
        raise NotImplementedError

    def multiplayer(
        self, player_choice_id: id, username: str, game_id: Optional[uuid.UUID] = None
    ):
        raise NotImplementedError


class RPSSLGameEngine(GameEngine):
    def __init__(
        self,
        games_service: GamesService,
        recent_games_service: RecentGamesService,
        user_game_info_service: UserGameInfoService,
    ):
        self.games_service = games_service
        self.recent_games_service = recent_games_service
        self.user_game_info_service = user_game_info_service
        self.rules = {
            Choice.ROCK: {Choice.LIZARD, Choice.SCISSORS},
            Choice.PAPER: {Choice.ROCK, Choice.SPOCK},
            Choice.SCISSORS: {Choice.PAPER, Choice.LIZARD},
            Choice.LIZARD: {Choice.SPOCK, Choice.PAPER},
            Choice.SPOCK: {Choice.SCISSORS, Choice.ROCK},
        }

    def single_player(self, player_choice_id: int, username: Optional[str] = None):
        player_name = username if username is not None else ANONYMOUS

        logging.info(
            f"Player {username} attempts to play game against {COMPUTER}, "
            f"choice: {player_choice_id}..."
        )
        computer_choice_id = utils.generate_random_choice_id()
        computer_choice = choices[computer_choice_id]

        player_choice = choices[player_choice_id]

        winner = self._resolve_winner(
            player_name, COMPUTER, player_choice, computer_choice
        )
        game = {
            "first_player": player_name,
            "first_player_choice": player_choice,
            "second_player": COMPUTER,
            "second_player_choice": computer_choice,
            "winner": winner,
            "game_id": uuid.uuid4(),
        }
        logging.info(f"{winner} wins game: {str(game['game_id'])}!")

        self.recent_games_service.add_game(game)
        if player_name != ANONYMOUS:
            self.user_game_info_service.add_game(game)

        return {
            "results": self._resolve_outcome(winner, player_name),
            "player": player_choice_id,
            "computer": computer_choice_id,
        }

    def multiplayer(
        self, player_choice_id: id, username: str, game_id: Optional[uuid.UUID] = None
    ):
        if game_id is None:
            logging.info(
                f"Player {username} attempts to play random game, "
                f"choice: {player_choice_id}..."
            )
            game = self.games_service.get_random_active_game()
        else:
            logging.info(
                f"Player {username} attempts to play game {game_id}, "
                f"choice: {player_choice_id}..."
            )
            game = self.games_service.get_active_game_by_id(game_id)
        if game is None:
            logging.exception("Error retrieving active game.")
            raise APIError(ActiveGameNotFoundError())

        game["second_player"] = username
        game["second_player_choice"] = player_choice_id

        winner = self._resolve_winner(
            game["first_player"],
            game["second_player"],
            choices[game["first_player_choice"]],
            choices[game["second_player_choice"]],
        )
        game["winner"] = winner
        logging.info(f"{winner} wins game: {game['game_id']}!")

        self.recent_games_service.add_game(game)
        self.user_game_info_service.add_game(game)
        self.games_service.complete_game(game["game_id"])

        return {
            "results": self._resolve_outcome(winner, username),
            game["second_player"]: game["second_player_choice"],
            game["first_player"]: game["first_player_choice"],
        }

    def _resolve_winner(
        self,
        first_player: str,
        second_player: str,
        first_player_choice: Choice,
        second_player_choice: Choice,
    ):
        choice_beats = self.rules[first_player_choice]

        if first_player_choice == second_player_choice:
            return GameResult.TIE
        elif second_player_choice in choice_beats:
            return first_player
        else:
            return second_player

    def _resolve_outcome(self, winner: str, user: str):
        if winner == user:
            return GameResult.WIN
        return GameResult.LOSS if winner != GameResult.TIE else GameResult.TIE
