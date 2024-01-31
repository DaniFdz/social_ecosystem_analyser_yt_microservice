import pytest


@pytest.fixture
def invalid_api_key():
    """Fixture for an invalid api key"""
    return "invalid_api_key"


@pytest.fixture
def topic():
    """Fixture for a topic"""
    return "gaming"
