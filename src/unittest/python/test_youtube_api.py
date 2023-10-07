from unittest import TestCase
from decouple import config
from src.main.python.SocialEcosystemAnalyser.youtube.youtube_api \
    import YoutubeAPI

YOUTUBE_API_KEY = config('YOUTUBE_API_KEY')

class TestApiResponse(TestCase):
    def test_api_response(self):
        """Test if the singleton works"""
        
        youtubeApi = YoutubeAPI(YOUTUBE_API_KEY)
        response = youtubeApi.videos_list_from_topic("videojuegos")

        self.assertTrue(response is not None)

