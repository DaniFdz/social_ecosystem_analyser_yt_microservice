from unittest import TestCase
from decouple import config
from src.main.python.SocialEcosystemAnalyser.virustTotal.check_url \
    import check_url
from src.main.python.SocialEcosystemAnalyser.\
    social_ecosystem_analyser_exception import \
    SocialEcosystemAnalyserException, MessageExceptions

VIRUSTOTAL_API_KEY = config('VIRUSTOTAL_API_KEY')

class TestVirusTotal(TestCase):
    def test_malicous_url(self):
        """Test a malicious url"""
        result = check_url(VIRUSTOTAL_API_KEY, "https://freebitco.in/signup/?op=s")
        self.assertTrue(result)

    def test_safe_url(self):
        """Test a safe url"""
        result = check_url(VIRUSTOTAL_API_KEY, "https://www.youtube.com")
        self.assertFalse(result)
    
    def test_wrong_api_key(self):
        """Test if the api key is wrong"""
        with self.assertRaises(SocialEcosystemAnalyserException) as context:
            check_url("invalid_api_key", "https://www.youtube.com")
        self.assertTrue(MessageExceptions.VIRUSTOTAL_API_ERROR in str(context.exception))