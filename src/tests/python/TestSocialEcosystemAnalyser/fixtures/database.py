import pytest

from src.main.python.SocialEcosystemAnalyser.database_management import \
    DatabaseManagement


@pytest.fixture
def database_management():
    """Fixture for DatabaseManagement"""
    dm = DatabaseManagement(test=True)
    return dm
