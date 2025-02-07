import abc
import collections
import heapq
from typing import Dict, List

from src.settings import settings
from src.singleton import Singleton


class InMemoryLeaderboardStore(metaclass=Singleton):
    def __init__(self):
        self._leaderboard = collections.defaultdict(int)

    def get_leaderboard(self):
        return self._leaderboard


class LeaderboardService(abc.ABC):
    def add_user_score(self, user: str, score: int):
        raise NotImplementedError

    def get_top_players(self, n=settings.LEADERBOARD_PLAYERS) -> List[Dict]:
        raise NotImplementedError


class InMemoryLeaderboardService(LeaderboardService):
    def __init__(self, store: InMemoryLeaderboardStore):
        self.store = store

    def add_user_score(self, user: str, score: int):
        self.store.get_leaderboard()[user] = score

    def get_top_players(self, n=settings.LEADERBOARD_PLAYERS):
        heap = []
        for user, score in self.store.get_leaderboard().items():
            if len(heap) < n:
                heapq.heappush(heap, (score, user))
            else:
                if score > heap[0][0]:
                    heapq.heappop(heap)
                    heapq.heappush(heap, (score, user))

        result = []
        while len(heap) > 0:
            item = heapq.heappop(heap)
            result.append({"name": item[1], "score": item[0]})

        return result[::-1]
