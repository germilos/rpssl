import abc
import collections
from typing import Dict

from src.enums import GameResult
from src.singleton import Singleton


class InMemoryUserGameInfoStore(metaclass=Singleton):
    def __init__(self):
        self._user_info = collections.defaultdict(
            lambda: {"games": [], "wins": 0, "losses": 0}
        )

    def get_user_info(self):
        return self._user_info


class UserGameInfoStorage(abc.ABC):
    def add_user_game(self, user: str, game: Dict, game_result: GameResult):
        raise NotImplementedError

    def get_all(self):
        raise NotImplementedError


class InMemoryUserGameInfoStorage(UserGameInfoStorage):
    def __init__(self, store: InMemoryUserGameInfoStore):
        self.store = store

    def add_user_game(self, user: str, game: Dict, game_result: GameResult):
        self.store.get_user_info()[user]["games"].append(game)

        if game_result == GameResult.WIN:
            self.store.get_user_info()[user]["wins"] += 1
        elif game_result == GameResult.LOSS:
            self.store.get_user_info()[user]["losses"] += 1

        return self.store.get_user_info()[user]

    def get_all(self):
        return self.store.get_user_info()
