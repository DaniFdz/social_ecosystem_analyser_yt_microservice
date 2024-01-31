import pytest
from decouple import config


@pytest.fixture
def youtube_api_key():
    """Fixture for YOUTUBE_API_KEY"""
    return config("YOUTUBE_API_KEY")
