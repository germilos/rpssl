from fastapi import Depends

from src.game_engine import GameEngine, RPSSLGameEngine
from src.services.games_service import GamesService
from src.services.leaderboard_service import (
    InMemoryLeaderboardStore,
    LeaderboardService,
    InMemoryLeaderboardService,
)
from src.services.scoreboard_service import RecentGamesService
from src.services.user_info_service import UserGameInfoService
from src.storage.games_storage import (
    GamesStorage,
    InMemoryGameStore,
    InMemoryGamesStorage,
)
from src.storage.recent_games_storage import (
    InMemoryRecentGamesStorage,
    RecentGamesStorage,
    InMemoryRecentGamesStore,
)
from src.storage.user_info_storage import (
    UserGameInfoStorage,
    InMemoryUserGameInfoStore,
    InMemoryUserGameInfoStorage,
)


def get_game_store() -> InMemoryGameStore:
    return InMemoryGameStore()


def get_games_storage(
    store: InMemoryGameStore = Depends(get_game_store),
) -> GamesStorage:
    return InMemoryGamesStorage(store=store)


def get_games_service(
    games_storage: GamesStorage = Depends(get_games_storage),
) -> GamesService:
    return GamesService(games_storage=games_storage)


def get_recent_games_store() -> InMemoryRecentGamesStore:
    return InMemoryRecentGamesStore()


def get_recent_games_storage(
    store: InMemoryRecentGamesStore = Depends(get_recent_games_store),
) -> RecentGamesStorage:
    return InMemoryRecentGamesStorage(store=store)


def get_recent_games_service(
    games_storage: RecentGamesStorage = Depends(get_recent_games_storage),
) -> RecentGamesService:
    return RecentGamesService(recent_games_storage=games_storage)


def get_leaderboard_store() -> InMemoryLeaderboardStore:
    return InMemoryLeaderboardStore()


def get_leaderboard_service(
    store: InMemoryLeaderboardStore = Depends(get_leaderboard_store),
) -> LeaderboardService:
    return InMemoryLeaderboardService(store=store)


def get_user_game_info_store() -> InMemoryUserGameInfoStore:
    return InMemoryUserGameInfoStore()


def get_user_game_info_storage(
    store: InMemoryUserGameInfoStore = Depends(get_user_game_info_store),
) -> UserGameInfoStorage:
    return InMemoryUserGameInfoStorage(store=store)


def get_user_game_info_service(
    storage: UserGameInfoStorage = Depends(get_user_game_info_storage),
    leaderboard_service=Depends(get_leaderboard_service),
) -> UserGameInfoService:
    return UserGameInfoService(
        user_game_info_storage=storage, leaderboard_service=leaderboard_service
    )


def get_game_engine(
    games_service: GamesService = Depends(get_games_service),
    recent_games_service=Depends(get_recent_games_service),
    user_game_info_service=Depends(get_user_game_info_service),
) -> GameEngine:
    return RPSSLGameEngine(
        games_service=games_service,
        recent_games_service=recent_games_service,
        user_game_info_service=user_game_info_service,
    )
