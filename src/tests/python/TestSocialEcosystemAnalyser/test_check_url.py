import pytest

from src.main.python.SocialEcosystemAnalyser.exceptions.social_ecosystem_analyser_exception import \
    SocialEcosystemAnalyserException
from src.main.python.SocialEcosystemAnalyser.exceptions.social_ecosystem_analyser_messages import \
    MessageExceptions
from src.main.python.SocialEcosystemAnalyser.virustTotal.check_url import \
    check_url


@pytest.mark.api
@pytest.mark.unittest
class TestCheckUrl:
    safe_url = "https://youtube.com"
    unsafe_url = "https://freebitco.in/signup/?op=s"

    def test_malicious_url(self, virustotal_api_key):
        """Test a malicious url"""
        result = check_url(virustotal_api_key, self.unsafe_url)
        assert result

    def test_safe_url(self, virustotal_api_key):
        """Test a safe url"""
        result = check_url(virustotal_api_key, self.safe_url)
        assert not result

    def test_wrong_api_key(self, invalid_api_key):
        """Test if the api key is wrong"""
        with pytest.raises(
                SocialEcosystemAnalyserException,
                match=MessageExceptions.VIRUSTOTAL_API_ERROR,
        ):
            check_url(invalid_api_key, self.safe_url)
