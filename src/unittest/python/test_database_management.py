from unittest import TestCase

from decouple import config

from src.main.python.SocialEcosystemAnalyser.database_management import \
    DatabaseManagement

YOUTUBE_API_KEY = config("YOUTUBE_API_KEY")


class TestDatabaseManagement(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dm = DatabaseManagement()

    @classmethod
    def tearDownClass(cls):
        cls.dm.__del__()

    def test_init(self):
        """Test if database management is initialized correctly"""
        self.assertTrue(self.dm is not None)

    def test_add_video(self):
        """"Test if a video is added correctly to the database"""
        videos = [{"test": "test"}]
        ids = self.dm.add_videos(*videos)
        self.assertIsNotNone(ids)
        self.assertEqual(len(ids), 1)
        self.dm.delete_videos(*ids)

    def test_add_videos(self):
        """Test if videos are added correctly to the database"""
        videos = [{"test": "test"}, {"test": "test"}]
        ids = self.dm.add_videos(*videos)
        self.assertTrue(ids is not None)
        self.assertEqual(len(ids), 2)
        self.dm.delete_videos(*ids)

    def test_get_video(self):
        """Test if a video is retrieved correctly from the database"""
        videos = [{"test": "test"}]
        ids = self.dm.add_videos(*videos)
        result = self.dm.get_videos()
        self.assertIsNotNone(result)
        self.assertEqual(result[-1].items(), videos[0].items())
        self.dm.delete_videos(*ids)

    def test_delete_video(self):
        """Test if a video is deleted correctly from the database"""
        videos = [{"test": "test"}]
        ids = self.dm.add_videos(*videos)
        self.assertEqual(self.dm.delete_videos(*ids), 1)

    def test_delete_videos(self):
        """Test if videos are deleted correctly from the database"""
        videos = [{"test": "test"}, {"test": "test"}]
        ids = self.dm.add_videos(*videos)
        self.assertEqual(self.dm.delete_videos(*ids), 2)
