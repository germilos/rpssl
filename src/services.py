import collections
from typing import Dict


class ScoreboardService:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.scoreboard = collections.deque(maxlen=capacity)

    def add(self, game: Dict):
        if len(self.scoreboard) == self.capacity:
            self.scoreboard.popleft()
        self.scoreboard.append(game)

    def reset(self):
        self.scoreboard.clear()

    def get_scoreboard(self):
        return list(self.scoreboard)
