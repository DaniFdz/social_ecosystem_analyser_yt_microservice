from unittest import TestCase
from decouple import config
from src.main.python.SocialEcosystemAnalyser.nlp.similar_topics_generation \
    import generate_topics
from src.main.python.SocialEcosystemAnalyser.\
    social_ecosystem_analyser_exception \
    import SocialEcosystemAnalyserException, MessageExceptions

COHERE_API_KEY = config('COHERE_API_KEY')

class TestSimilarTopicsGeneration(TestCase):
    def test_generate_topics(self):
        topics = generate_topics("games", COHERE_API_KEY)
        self.assertTrue(topics is not None)
        self.assertTrue(len(topics) == 5)
    
    def test_invalid_api(self):
        with self.assertRaises(SocialEcosystemAnalyserException) as context:
            generate_topics("games", "invalid_api_key")
        self.assertTrue(MessageExceptions.COHERE_API_ERROR in str(context.exception))
