import pytest

from src.main.python.SocialEcosystemAnalyser.exceptions.social_ecosystem_analyser_exception import \
    SocialEcosystemAnalyserException
from src.main.python.SocialEcosystemAnalyser.exceptions.social_ecosystem_analyser_messages import \
    MessageExceptions
from src.main.python.SocialEcosystemAnalyser.nlp.similar_topics_generation import \
    generate_topics


@pytest.mark.api
@pytest.mark.unittest
class TestSimilarTopicsGenerator:
    topic = "gaming"

    def test_generate_topics(self):
        """Test if the topics are generated correctly"""
        topics = generate_topics(self.topic)
        assert topics is not None
        assert len(topics) == 5

    def test_invalid_api(self, mocker, invalid_api_key):
        """Test if the api key is wrong"""
        mocker.patch("os.environ.get", return_value=invalid_api_key)
        with pytest.raises(SocialEcosystemAnalyserException,
                           match=MessageExceptions.COHERE_API_ERROR):
            generate_topics(self.topic)
