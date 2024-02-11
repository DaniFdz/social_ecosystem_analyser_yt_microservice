import pytest

from src.main.python.SocialEcosystemAnalyser.database_management import \
    DatabaseManagement


@pytest.mark.unittest
class TestSingleton:
    def test_singleton(self):
        """Test if the singleton works"""
        db1 = DatabaseManagement()
        db2 = DatabaseManagement()
        assert db1 == db2
