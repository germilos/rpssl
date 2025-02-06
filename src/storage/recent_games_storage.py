import abc
import collections
from typing import Dict, List

from src.settings import settings
from src.singleton import Singleton


class InMemoryRecentGamesStore(metaclass=Singleton):
    def __init__(self):
        self._capacity = settings.MAX_RECENT_GAMES
        self._games = collections.deque(maxlen=self._capacity)

    def get_games(self) -> collections.deque:
        return self._games

    def get_capacity(self) -> int:
        return self._capacity


class RecentGamesStorage(abc.ABC):
    def add(self, game: Dict) -> Dict:
        raise NotImplementedError

    def clear(self) -> Dict:
        raise NotImplementedError

    def get_all(self) -> List[Dict]:
        raise NotImplementedError


class InMemoryRecentGamesStorage(RecentGamesStorage):
    def __init__(self, store: InMemoryRecentGamesStore):
        self.store = store

    def add(self, game: Dict):
        if len(self.store.get_games()) == self.store.get_capacity():
            self.store.get_games().popleft()
        self.store.get_games().append(game)

    def clear(self):
        self.store.get_games().clear()

    def get_all(self) -> List[Dict]:
        return list(self.store.get_games())[::-1]
