import requests

from src.enums import choices
from src.settings import settings


def fetch_random_number():
    headers = {"Accept": "application/json"}

    response = requests.get(settings.RANDOM_GENERATOR_URL, headers=headers)

    print(response.status_code)

    return (response.json()["random_number"] % len(choices)) + 1
