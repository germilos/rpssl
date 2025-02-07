import abc
import uuid
from collections import defaultdict
from typing import Dict, List, Optional

from src.exceptions import ActiveGamesLimitError, APIError
from src.settings import settings
from src.singleton import Singleton
from src.utils import generate_uuid


class InMemoryGameStore(metaclass=Singleton):
    def __init__(self):
        self._capacity = settings.MAX_ACTIVE_GAMES
        self._active_games = defaultdict(None)
        self._completed_games = defaultdict(None)

    def get_active_games(self) -> Dict:
        return self._active_games

    def get_completed_games(self) -> Dict:
        return self._completed_games

    def get_capacity(self) -> int:
        return self._capacity


class GamesStorage(abc.ABC):
    def create_active_game(self, new_game: Dict) -> Dict:
        raise NotImplementedError

    def get_active_game_by_id(self, game_id: uuid.UUID) -> Dict:
        raise NotImplementedError

    def get_active_games(self) -> List[Dict]:
        raise NotImplementedError

    def remove_active_game(self, game_id: uuid.UUID):
        raise NotImplementedError

    def add_completed_game(self, completed_game: Dict) -> uuid.UUID:
        raise NotImplementedError

    def get_completed_games(self) -> List[Dict]:
        raise NotImplementedError


class InMemoryGamesStorage(GamesStorage):
    def __init__(self, store: InMemoryGameStore):
        self.store = store

    def create_active_game(self, new_game: Dict) -> Dict:
        if len(self.store.get_active_games()) == self.store.get_capacity():
            raise APIError(ActiveGamesLimitError())

        new_game_id = generate_uuid()
        new_game["game_id"] = new_game_id
        self.store.get_active_games()[new_game_id] = new_game

        return new_game

    def get_active_game_by_id(self, game_id: uuid.UUID) -> Optional[Dict]:
        return self.store.get_active_games()[game_id]

    def get_active_games(self):
        result = []
        for value in self.store.get_active_games().values():
            result.append(value)
        return result

    def get_completed_games(self) -> List[Dict]:
        result = []
        for value in self.store.get_completed_games().values():
            result.append(value)
        return result

    def remove_active_game(self, game_id: uuid.UUID):
        del self.store.get_active_games()[game_id]

    def add_completed_game(self, game: Dict):
        self.store.get_completed_games()[game["game_id"]] = game
