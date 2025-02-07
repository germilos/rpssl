import pytest
from starlette.testclient import TestClient

from src.main import app


@pytest.fixture
def client() -> TestClient:
    """
    Fixture that returns an unauthenticated API Client
    """
    return TestClient(app)
