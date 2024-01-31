import pytest

from src.main.python.SocialEcosystemAnalyser.nlp.similar_topics_generation import \
    generate_topics
from src.main.python.SocialEcosystemAnalyser.social_ecosystem_analyser_exception import (
    MessageExceptions, SocialEcosystemAnalyserException)


def test_generate_topics(cohere_api_key, topic):
    """Test if the topics are generated correctly"""
    topics = generate_topics(topic, cohere_api_key)
    assert topics is not None
    assert len(topics) == 5


def test_invalid_api(invalid_api_key, topic):
    """Test if the api key is wrong"""
    with pytest.raises(SocialEcosystemAnalyserException,
                       match=MessageExceptions.COHERE_API_ERROR):
        generate_topics(topic, invalid_api_key)
