from unittest import TestCase
from decouple import config
from src.main.python.SocialEcosystemAnalyser.youtube.youtube_api \
    import YoutubeAPI
from src.main.python.SocialEcosystemAnalyser.\
    social_ecosystem_analyser_exception \
    import SocialEcosystemAnalyserException, MessageExceptions

YOUTUBE_API_KEY = config('YOUTUBE_API_KEY')

class TestApiResponse(TestCase):
    def test_api_response(self):
        """Test if the api response is correct"""
        
        youtubeApi = YoutubeAPI(YOUTUBE_API_KEY)
        response = youtubeApi._videos_list_from_topic("games", None)

        self.assertTrue(response is not None)
    
    def test_invalid_api_key(self):
        """Test if the api key is wrong"""
        with self.assertRaises(SocialEcosystemAnalyserException) as context:
            youtubeApi = YoutubeAPI('invalid_api_key')
            youtubeApi._videos_list_from_topic("games", None)
        self.assertTrue(MessageExceptions.YOUTUBE_API_KEY_ERROR in str(context.exception))

