from src.main.python.SocialEcosystemAnalyser.database_management import \
    DatabaseManagement


def test_singleton_vaccinemanager():
    """Test if the singleton works"""
    db1 = DatabaseManagement()
    db2 = DatabaseManagement()
    assert db1 == db2
