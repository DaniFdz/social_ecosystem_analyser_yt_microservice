import pytest

from src.main.python.SocialEcosystemAnalyser.database_management import \
    DatabaseManagement


@pytest.fixture
def database_management():
    """Fixture for DatabaseManagement"""
    dm = DatabaseManagement(test=True)
    return dm


@pytest.fixture
def single_item():
    """Fixture for a single item to insert"""
    return [{"test": "test"}]


@pytest.fixture
def multiple_items():
    """Fixture for multiple items to insert"""
    return [{"test": "test"}, {"test": "test"}]
