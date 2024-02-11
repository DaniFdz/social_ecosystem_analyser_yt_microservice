import os

import pytest


@pytest.fixture
def youtube_api_key():
    """Fixture for YOUTUBE_API_KEY"""
    return os.environ.get("YOUTUBE_API_KEY")
