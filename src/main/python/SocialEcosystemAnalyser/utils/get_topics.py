import logging
import os
from typing import List

from src.main.python.SocialEcosystemAnalyser.exceptions.social_ecosystem_analyser_exception import \
    SocialEcosystemAnalyserException
from src.main.python.SocialEcosystemAnalyser.nlp.similar_topics_generation import \
    generate_topics
from src.main.python.SocialEcosystemAnalyser.settings import LOGGING

from .exit_program import ExitProgram

logging.basicConfig(format=LOGGING["formatters"]["standard"]["format"])


class GetTopics:
    @classmethod
    def __pop_topic_from_file(cls) -> str:
        """Read the new topic from the topics.txt file"""
        if not os.path.exists("topics.txt"):
            logging.error("File topics.txt not found")
            ExitProgram.exit_program(1)

        with open("topics.txt", "r") as file:
            topics = file.readline().strip()

        if topics == "":
            logging.error("sNo topics found in topics.txt")
            ExitProgram.exit_program(1)

        topic = topics[0].strip()

        with open("topics.txt", "w") as file:
            file.writelines(file.readlines()[1:])

        return topic

    @classmethod
    def __generate_topics_from(cls, topic: str) -> List[str]:
        try:
            topics = generate_topics(topic)
        except SocialEcosystemAnalyserException as e:
            logging.error(e)
            if input("Do you want to continue? (Y/n): ").lower() == "n":
                ExitProgram.exit_program(1)
            topics = [topic]

        return topics

    @classmethod
    def get_topics(cls) -> List[str]:
        topic = cls.__pop_topic_from_file()

        topics = cls.__generate_topics_from(topic)

        logging.info(f"Testing topics: {topics}")
        return topics
