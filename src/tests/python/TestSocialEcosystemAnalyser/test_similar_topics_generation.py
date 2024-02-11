import pytest

from src.main.python.SocialEcosystemAnalyser.exceptions.social_ecosystem_analyser_exception import (
    MessageExceptions, SocialEcosystemAnalyserException)
from src.main.python.SocialEcosystemAnalyser.nlp.similar_topics_generation import \
    generate_topics


@pytest.mark.api
@pytest.mark.unittest
class TestSimilarTopicsGenerator:
    topic = "gaming"

    def test_generate_topics(self, cohere_api_key):
        """Test if the topics are generated correctly"""
        topics = generate_topics(self.topic, cohere_api_key)
        assert topics is not None
        assert len(topics) == 5

    def test_invalid_api(self, invalid_api_key):
        """Test if the api key is wrong"""
        with pytest.raises(SocialEcosystemAnalyserException,
                           match=MessageExceptions.COHERE_API_ERROR):
            generate_topics(self.topic, invalid_api_key)
