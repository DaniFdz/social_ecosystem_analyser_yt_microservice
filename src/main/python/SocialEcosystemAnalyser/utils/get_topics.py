import logging
from typing import List

from src.main.python.SocialEcosystemAnalyser.database.topics.api_topics_repository import \
    ApiTopicsRepository
from src.main.python.SocialEcosystemAnalyser.database.topics.topics_repository import \
    Topic


class GetTopics:
    @classmethod
    def get_topics(cls) -> List[Topic]:
        topics = list(
            [t for t in ApiTopicsRepository.get_topics() if not t.finished])

        return topics
