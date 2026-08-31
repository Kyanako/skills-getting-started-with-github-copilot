"""
Shared test configuration and fixtures for FastAPI integration tests.
"""
import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """
    Provides a TestClient instance for making HTTP requests to the FastAPI app.
    This fixture is automatically used by all test functions.
    """
    return TestClient(app)
