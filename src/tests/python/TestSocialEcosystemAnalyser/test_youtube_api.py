import pytest

from src.main.python.SocialEcosystemAnalyser.exceptions.social_ecosystem_analyser_exception import \
    SocialEcosystemAnalyserException
from src.main.python.SocialEcosystemAnalyser.exceptions.social_ecosystem_analyser_messages import \
    MessageExceptions
from src.main.python.SocialEcosystemAnalyser.youtube.youtube_api import \
    YoutubeAPI


@pytest.mark.api
@pytest.mark.unittest
class TestYoutubeAPI:
    topic = "gaming"

    def test_api_response(self, youtube_api_key):
        """Test if the api response is correct"""
        youtube_api = YoutubeAPI(youtube_api_key)
        response = youtube_api._videos_list_from_topic(self.topic, None)
        assert response is not None

    def test_invalid_api_key(self, invalid_api_key):
        """Test if the api key is wrong"""
        with pytest.raises(
                SocialEcosystemAnalyserException,
                match=MessageExceptions.YOUTUBE_API_KEY_ERROR,
        ):
            youtube_api = YoutubeAPI(invalid_api_key)
            youtube_api._videos_list_from_topic(self.topic, None)
