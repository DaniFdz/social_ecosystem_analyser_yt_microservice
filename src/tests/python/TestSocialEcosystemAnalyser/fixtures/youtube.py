import os

import pytest
from dotenv import load_dotenv


@pytest.fixture
def youtube_api_key():
    """Fixture for YOUTUBE_API_KEY"""
    load_dotenv()
    return os.environ.get("YOUTUBE_API_KEY")
