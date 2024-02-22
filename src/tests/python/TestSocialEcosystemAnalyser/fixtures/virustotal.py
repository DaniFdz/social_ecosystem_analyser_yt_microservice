import os

import pytest
from dotenv import load_dotenv


@pytest.fixture
def virustotal_api_key():
    """Fixture for VIRUSTOTAL_API_KEY"""
    load_dotenv()
    return os.environ.get("VIRUSTOTAL_API_KEY")
