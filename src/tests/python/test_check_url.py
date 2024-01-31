import pytest

from src.main.python.SocialEcosystemAnalyser.social_ecosystem_analyser_exception import (
    MessageExceptions, SocialEcosystemAnalyserException)
from src.main.python.SocialEcosystemAnalyser.virustTotal.check_url import \
    check_url


def test_malicious_url(virustotal_api_key, unsafe_url):
    """Test a malicious url"""
    result = check_url(virustotal_api_key, unsafe_url)
    assert result


def test_safe_url(virustotal_api_key, safe_url):
    """Test a safe url"""
    result = check_url(virustotal_api_key, safe_url)
    assert not result


def test_wrong_api_key(invalid_api_key, safe_url):
    """Test if the api key is wrong"""
    with pytest.raises(SocialEcosystemAnalyserException,
                       match=MessageExceptions.VIRUSTOTAL_API_ERROR):
        check_url(invalid_api_key, safe_url)
