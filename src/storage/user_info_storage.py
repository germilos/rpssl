import abc
import collections
from typing import Dict

from src.singleton import Singleton


class InMemoryUserGameInfoStore(metaclass=Singleton):
    def __init__(self):
        self._user_info = collections.defaultdict(lambda: {"games": [], "wins": 0, "losses": 0, "ratio": 0})

    def get_user_info(self):
        return self._user_info


class UserGameInfoStorage(abc.ABC):
    def add_user_win(self, user: str, game: Dict):
        raise NotImplementedError

    def add_user_loss(self, user: str, game: Dict):
        raise NotImplementedError


class InMemoryUserGameInfoStorage(UserGameInfoStorage):
    def __init__(self, store: InMemoryUserGameInfoStore):
        self.store = store

    def add_user_win(self, user: str, game: Dict):
        if user in self.store.get_user_info():
            self.store.get_user_info()[user]["games"].append(game)
        else:
            self.store.get_user_info()[user]["games"] = [game]
        self.store.get_user_info()[user]["wins"] += 1

        return self.store.get_user_info()[user]

    def add_user_loss(self, user: str, game: Dict):
        if user in self.store.get_user_info():
            self.store.get_user_info()[user]["games"].append(game)
        else:
            self.store.get_user_info()[user]["games"].append(game)
        self.store.get_user_info()[user]["losses"] += 1

        return self.store.get_user_info()[user]
