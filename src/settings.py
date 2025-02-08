import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    RANDOM_GENERATOR_URL: str = "https://codechallenge.boohma.com/random"
    RANDOM_NUMBER_RETRIEVAL_ATTEMPTS: int = 5
    MAX_RECENT_GAMES: int = 10
    LEADERBOARD_PLAYERS: int = 10
    MAX_ACTIVE_GAMES: int = 10
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


settings = Settings()
