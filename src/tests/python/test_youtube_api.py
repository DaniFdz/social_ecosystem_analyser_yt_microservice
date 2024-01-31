import pytest

from src.main.python.SocialEcosystemAnalyser.social_ecosystem_analyser_exception import (
    MessageExceptions, SocialEcosystemAnalyserException)
from src.main.python.SocialEcosystemAnalyser.youtube.youtube_api import \
    YoutubeAPI


def test_api_response(youtube_api_key, topic):
    """Test if the api response is correct"""
    youtube_api = YoutubeAPI(youtube_api_key)
    response = youtube_api._videos_list_from_topic(topic, None)
    assert response is not None


def test_invalid_api_key(invalid_api_key, topic):
    """Test if the api key is wrong"""
    with pytest.raises(SocialEcosystemAnalyserException,
                       match=MessageExceptions.YOUTUBE_API_KEY_ERROR):
        youtube_api = YoutubeAPI(invalid_api_key)
        youtube_api._videos_list_from_topic(topic, None)
