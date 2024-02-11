import os

import pytest


@pytest.fixture
def virustotal_api_key():
    """Fixture for VIRUSTOTAL_API_KEY"""
    return os.environ.get("VIRUSTOTAL_API_KEY")
