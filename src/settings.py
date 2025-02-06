from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    RANDOM_GENERATOR_URL: str = "https://codechallenge.boohma.com/random"
    RANDOM_NUMBER_RETRIEVAL_ATTEMPTS: int = 5
    SCOREBOARD_STORAGE_MAX_LENGTH: int = 10
    LEADERBOARD_PLAYERS: int = 10
    MAX_ACTIVE_GAMES: int = 10


settings = Settings()
