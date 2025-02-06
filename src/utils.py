import requests
import logging

from src.choices import choices
from src.exceptions import RandomNumberRetrievalError
from src.settings import settings


def fetch_random_number():
    retries = 0
    while retries < settings.RANDOM_NUMBER_RETRIEVAL_ATTEMPTS:
        try:
            headers = {"Accept": "application/json"}

            response = requests.get(settings.RANDOM_GENERATOR_URL, headers=headers)
            random_number = response.json()["random_number"]
            return (random_number % len(choices)) + 1
        except Exception as e:
            retries += 1
            retries_left = settings.RANDOM_NUMBER_RETRIEVAL_ATTEMPTS - retries
            logging.exception(
                f"Error occurred while retrieving random number: {e}."
                f" {retries_left} retries left"
            )
    raise RandomNumberRetrievalError
