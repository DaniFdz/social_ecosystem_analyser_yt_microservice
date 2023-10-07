from unittest import TestCase
from src.main.python.SocialEcosystemAnalyser.database_management \
    import DatabaseManagement

class TestSingleton(TestCase):
    def test_singleton_vaccinemanager(self):
        """Test if the singleton works"""
        db1 = DatabaseManagement()
        db2 = DatabaseManagement()
        self.assertEqual(db1, db2)

