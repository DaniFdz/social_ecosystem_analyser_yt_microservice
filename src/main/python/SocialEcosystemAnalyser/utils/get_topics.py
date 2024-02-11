import os
from typing import List

from src.main.python.SocialEcosystemAnalyser.exceptions.social_ecosystem_analyser_exception import \
    SocialEcosystemAnalyserException
from src.main.python.SocialEcosystemAnalyser.nlp.similar_topics_generation import \
    generate_topics

from .exit_program import ExitProgram


class GetTopics:
    @classmethod
    def __pop_topic_from_file(cls) -> str:
        """Read the new topic from the topics.txt file"""
        if not os.path.exists("topics.txt"):
            print("[!] File topics.txt not found")
            ExitProgram.exit_program(1)

        with open("topics.txt", "r") as file:
            topics = file.readline().strip()

        if topics == "":
            print("[!] No topics found in topics.txt")
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
            print(e)
            if input("Do you want to continue? (Y/n): ").lower() == "n":
                ExitProgram.exit_program()
            topics = [topic]

        return topics

    @classmethod
    def get_topics(cls) -> List[str]:
        topic = cls.__pop_topic_from_file()

        topics = cls.__generate_topics_from(topic)

        print(f"[i] Testing topics: {topics}")
        return topics
