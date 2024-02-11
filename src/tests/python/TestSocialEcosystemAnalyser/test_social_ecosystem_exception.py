import pytest

from src.main.python.SocialEcosystemAnalyser.exceptions.social_ecosystem_analyser_exception import \
    SocialEcosystemAnalyserException
from src.main.python.SocialEcosystemAnalyser.exceptions.social_ecosystem_analyser_messages import \
    MessageExceptions


@pytest.mark.unittest
class TestSocialEcosystemException:
    def test_exception_message(self):
        """Test if the exception message is correct"""
        with pytest.raises(SocialEcosystemAnalyserException,
                           match=MessageExceptions.YOUTUBE_API_ERROR):
            raise SocialEcosystemAnalyserException(
                MessageExceptions.YOUTUBE_API_ERROR)

    def test_exception_message_setter(self):
        """Test if the exception message is set correctly"""
        with pytest.raises(SocialEcosystemAnalyserException,
                           match="Test message changed"):

            exception = SocialEcosystemAnalyserException("Test message")
            exception.message = "Test message changed"
            raise exception
