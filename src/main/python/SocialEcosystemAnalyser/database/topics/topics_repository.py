from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass
class Topic:
    name: str
    finished: bool
    next_page_token: str


class TopicsRepository(ABC):
    @abstractmethod
    def check_health(self) -> bool:
        pass

    @abstractmethod
    def get_topics(self) -> List[Topic]:
        pass

    @abstractmethod
    def get_topic_by_name(cls, topic_name: str) -> Topic | None:
        pass

    @abstractmethod
    def create_topic(self, topic_name: str) -> bool:
        pass

    @abstractmethod
    def set_topic_as_finished(cls, topic: Topic) -> bool:
        pass

    @abstractmethod
    def save_next_page_token(cls, topic_name: str, token: str) -> bool:
        pass
