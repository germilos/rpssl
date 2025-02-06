import abc
import collections
from typing import Dict, List

from src.settings import settings
from src.singleton import Singleton


class InMemoryScoreboardStore(metaclass=Singleton):
    def __init__(self):
        self._capacity = settings.SCOREBOARD_STORAGE_MAX_LENGTH
        self._scoreboard = collections.deque(maxlen=self._capacity)

    def get_scoreboard(self) -> collections.deque:
        return self._scoreboard

    def get_capacity(self) -> int:
        return self._capacity


class ScoreboardStorage(abc.ABC):
    def add(self, game: Dict) -> Dict:
        raise NotImplementedError

    def clear(self) -> Dict:
        raise NotImplementedError

    def get_all(self) -> List[Dict]:
        raise NotImplementedError


class InMemoryScoreboardStorage(ScoreboardStorage):
    def __init__(self, store: InMemoryScoreboardStore):
        self.store = store

    def add(self, game: Dict):
        if len(self.store.get_scoreboard()) == self.store.get_capacity():
            self.store.get_scoreboard().popleft()
        self.store.get_scoreboard().append(game)

    def clear(self):
        self.store.get_scoreboard().clear()

    def get_all(self) -> List[Dict]:
        return list(self.store.get_scoreboard())[::-1]
