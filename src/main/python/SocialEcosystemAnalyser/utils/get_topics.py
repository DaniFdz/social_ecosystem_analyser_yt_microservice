import logging
import sys
from typing import List

from src.main.python.SocialEcosystemAnalyser.database.topics.api_topics_repository import \
    ApiTopicsRepository
from src.main.python.SocialEcosystemAnalyser.database.topics.topics_repository import \
    Topic
from src.main.python.SocialEcosystemAnalyser.exceptions.social_ecosystem_analyser_exception import \
    SocialEcosystemAnalyserException
from src.main.python.SocialEcosystemAnalyser.nlp.similar_topics_generation import \
    generate_topics
from src.main.python.SocialEcosystemAnalyser.settings import LOGGING

logging.basicConfig(format=LOGGING["formatters"]["standard"]["format"])


class GetTopics:
    @classmethod
    def __pop_topic(cls) -> None:
        """ "Pop the first non finished topic from the database"""
        topics = ApiTopicsRepository.get_topics()
        for topic in topics:
            if not topic.finished:
                return topic
        return None

    @classmethod
    def __generate_topics_from(cls, topic: str) -> List[str]:
        """
        Generate similar topics from the given topic. If cohere API is not available,
        it will return the same topic as a list.

        @param topic: str
        @return: List[str]
        """
        try:
            topics = generate_topics(topic)
        except SocialEcosystemAnalyserException:
            topics = [topic]

        return topics

    @classmethod
    def get_topics(cls) -> List[Topic]:
        topic = cls.__pop_topic()
        if topic is None:
            logging.error("No topics to analyse")
            sys.exit(1)

        topics = cls.__generate_topics_from(topic.name)

        for t in topics:
            if ApiTopicsRepository.get_topic_by_name(t) is None:
                ApiTopicsRepository.create_topic(t)

        topics_list = [
            x for x in
            [ApiTopicsRepository.get_topic_by_name(t) for t in topics]
            if x is not None and x.finished is False
        ]

        logging.info(f"Testing topics: {topics_list}")
        return topics_list
