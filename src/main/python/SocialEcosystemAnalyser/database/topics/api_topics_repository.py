import os
from typing import List

import requests as r
from dotenv import load_dotenv

from .topics_repository import Topic, TopicsRepository


class ApiTopicsRepository(TopicsRepository):
    load_dotenv()
    __api = os.environ.get("API_URL", "http://localhost:3000/")
    __endpoint = "api/v1/topics/"
    __token = os.environ.get("API_TOKEN", "")

    @classmethod
    def get_topics(cls) -> List[Topic]:
        """
        Fetches GET /api/v1/topics/

        @return: List[Topic]: List of topics
        """
        endpoint = cls.__api + cls.__endpoint
        res = r.get(
            endpoint,
            headers={"Authorization": f"Bearer {cls.__token}"},
        )

        if res.status_code != 200:
            return []

        data = list([
            Topic(topic["name"], topic["finished"], topic["next_page_token"])
            for topic in res.json()["data"]
        ])
        return data

    @classmethod
    def get_topic_by_name(cls, topic_name: str) -> Topic | None:
        """
        Fetches GET /api/v1/topics/{topic}

        @param: topic (str): Topic to fetch

        @return: Topic: Topic data
        """
        endpoint = cls.__api + cls.__endpoint + topic_name
        res = r.get(
            endpoint,
            headers={"Authorization": f"Bearer {cls.__token}"},
        )

        if res.status_code != 200:
            return None

        data = res.json()
        return Topic(data["name"], data["finished"], data["next_page_token"])

    @classmethod
    def create_topic(cls, topic_name: str) -> bool:
        """
        Fetches POST /api/v1/topics/

        @param: topic_name (str): Topic to create

        @return: bool: If the topic was created
        """
        endpoint = cls.__api + cls.__endpoint
        res = r.post(
            endpoint,
            headers={"Authorization": f"Bearer {cls.__token}"},
            json={
                "name": topic_name,
                "finished": False,
                "next_page_token": ""
            },
        )

        return res.status_code == 201

    @classmethod
    def __update_topic(cls, topic: Topic) -> bool:
        """
        Fetches PUT /api/v1/topics/:topic_name

        @param: topic (Topic): Topic data

        @return: bool: If the topic was updated
        """
        endpoint = cls.__api + cls.__endpoint + topic.name
        res = r.put(
            endpoint,
            headers={"Authorization": f"Bearer {cls.__token}"},
            json={
                "name": topic.name,
                "finished": topic.finished,
                "next_page_token": topic.next_page_token
            },
        )

        return res.status_code == 200

    @classmethod
    def set_topic_as_finished(cls, topic: Topic) -> bool:
        """
        Fetches PUT /api/v1/topics/

        @param: topic (Topic): Topic to set as finished

        @return: bool: If the topic was updated
        """
        topic.finished = True
        return cls.__update_topic(topic)

    @classmethod
    def save_next_page_token(cls, topic_name: str, token: str) -> bool:
        """
        Fetches PUT /api/v1/topics/

        @param: topic_name (str): Topic to save the next page token to

        @return: bool: If the topic was updated
        """
        topic = Topic(topic_name, False, token)
        return cls.__update_topic(topic)
