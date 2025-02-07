import pytest
from starlette.testclient import TestClient

from src.main import app


@pytest.fixture
def client() -> TestClient:
    """
    Fixture that returns an unauthenticated API Client
    """
    return TestClient(app)


def pytest_sessionstart(session):  # noqa
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
