import logging
from enum import Enum
from logging import config
from typing import Optional, Any

from pydantic import PostgresDsn, field_validator, ValidationInfo
from pydantic_settings import BaseSettings


class Environment(str, Enum):
    DEVELOPMENT = "development"
    TEST = "test"
    STAGING = "staging"
    PRODUCTION = "production"


class Settings(BaseSettings):
    RANDOM_GENERATOR_URL: str = "https://codechallenge.boohma.com/random"
    
    # DB_HOST: str
    # DB_PORT: int
    # DB_NAME: str
    # DB_USER: str
    # DB_PASSWORD: str
    # DB_CONNECTION: Optional[PostgresDsn] = None
    # DB_CONNECTION_POOL_SIZE: int = 100
    # DB_CONNECTION_POOL_OVERFLOW: int = 20
    #
    # @field_validator("DB_CONNECTION")
    # def assemble_db_connection(cls, v: Optional[str], values: ValidationInfo) -> Any:
    #     if isinstance(v, str):
    #         return v
    #
    #     variables = values.data
    #
    #     db_url = PostgresDsn.build(
    #         scheme="postgresql",
    #         host=variables.get("DB_HOST"),
    #         port=variables.get("DB_PORT"),
    #         path=variables.get("DB_NAME"),
    #         username=variables.get("DB_USER"),
    #         password=variables.get("DB_PASSWORD"),
    #     )
    #     return db_url


settings = Settings()
