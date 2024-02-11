import os

import pytest


@pytest.fixture
def cohere_api_key():
    """Fixture for COHERE_API_KEY"""
    return os.environ.get("COHERE_API_KEY")
