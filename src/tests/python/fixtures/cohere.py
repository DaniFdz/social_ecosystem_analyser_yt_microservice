import pytest
from decouple import config


@pytest.fixture
def cohere_api_key():
    """Fixture for COHERE_API_KEY"""
    return config("COHERE_API_KEY")
