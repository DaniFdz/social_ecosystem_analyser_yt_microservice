import pytest
from decouple import config


@pytest.fixture
def virustotal_api_key():
    """Fixture for VIRUSTOTAL_API_KEY"""
    return config("VIRUSTOTAL_API_KEY")


@pytest.fixture
def safe_url():
    """Fixture for a safe url"""
    return "https://youtube.com"


@pytest.fixture
def unsafe_url():
    """Fixture for an unsafe url"""
    return "https://freebitco.in/signup/?op=s"
