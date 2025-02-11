import logging
import pickle

import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src import api
from src.services.leaderboard_service import (
    InMemoryLeaderboardStore,
    InMemoryLeaderboardService,
)
from src.services.recent_games_service import RecentGamesService
from src.services.user_game_info_service import UserGameInfoService
from src.settings import settings
from src.storage.recent_games_storage import (
    InMemoryRecentGamesStorage,
    InMemoryRecentGamesStore,
)
from src.storage.user_info_storage import (
    InMemoryUserGameInfoStorage,
    InMemoryUserGameInfoStore,
)

logging.basicConfig(level=logging.INFO)

PERSISTENCE_FILES_PREFIX = f"{settings.BASE_DIR}/src/persistence_files"
RECENT_GAMES_FILE = "recent_games.pkl"
LEADERBOARD_FILE = "leaderboard.pkl"
USER_GAMES_FILE = "user_games.pkl"


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        with (
            open(f"{PERSISTENCE_FILES_PREFIX}/{RECENT_GAMES_FILE}", "rb") as rg,
            open(f"{PERSISTENCE_FILES_PREFIX}/{LEADERBOARD_FILE}", "rb") as lb,
            open(f"{PERSISTENCE_FILES_PREFIX}/{USER_GAMES_FILE}", "rb") as ug,
        ):
            logging.info("Loading RPSSL data from files...")
            recent_games_service = RecentGamesService(
                InMemoryRecentGamesStorage(InMemoryRecentGamesStore())
            )
            recent_games_dicts = pickle.load(rg)
            recent_games_service.add_games(recent_games_dicts[::-1])

            leaderboard_service = InMemoryLeaderboardService(InMemoryLeaderboardStore())
            user_score_dicts = pickle.load(lb)
            for us in user_score_dicts:
                leaderboard_service.add_user_score(us["user"], us["score"])

            user_games_service = UserGameInfoService(
                InMemoryUserGameInfoStorage(InMemoryUserGameInfoStore()),
                leaderboard_service,
            )
            user_games = pickle.load(ug)
            user_games_store = user_games_service.get_all_games()
            for user, games in user_games.items():
                user_games_store[user] = games
            logging.info("Finished loading RPSSL data!")
    except EOFError as e:
        logging.warning(f"App state files empty, initializing empty state. {e}")
    except Exception as e:
        logging.exception(e)
    yield
    try:
        with (
            open(f"{PERSISTENCE_FILES_PREFIX}/{RECENT_GAMES_FILE}", "wb+") as rg,
            open(f"{PERSISTENCE_FILES_PREFIX}/{LEADERBOARD_FILE}", "wb+") as lb,
            open(f"{PERSISTENCE_FILES_PREFIX}/{USER_GAMES_FILE}", "wb+") as ug,
        ):
            logging.info("Dumping RPSSL data to files...")
            recent_games_service = RecentGamesService(
                InMemoryRecentGamesStorage(InMemoryRecentGamesStore())
            )
            recent_games = [
                recent_game.to_dict()
                for recent_game in recent_games_service.get_recent_games()
            ]
            pickle.dump(recent_games, rg)

            leaderboard_service = InMemoryLeaderboardService(InMemoryLeaderboardStore())
            leaderboard = [
                user_score.to_dict()
                for user_score in leaderboard_service.get_leaderboard()
            ]
            pickle.dump(leaderboard, lb)

            user_games_service = UserGameInfoService(
                InMemoryUserGameInfoStorage(InMemoryUserGameInfoStore()),
                leaderboard_service,
            )
            user_games = dict(user_games_service.get_all_games())
            pickle.dump(user_games, ug)
            logging.info("Finished dumping RPSSL data!")
    except Exception as e:
        logging.exception(e)


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.router, prefix="/api/v1")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9500, reload=True)
