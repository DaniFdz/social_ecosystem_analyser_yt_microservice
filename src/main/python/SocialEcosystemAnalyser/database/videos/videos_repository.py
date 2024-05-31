from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass
class Comment:
    is_author: bool
    text: str
    like_count: int

    def to_dict(self):
        return {
            "is_author": self.is_author,
            "text": self.text,
            "like_count": self.like_count,
        }


@dataclass
class Video:
    topic: str
    description: str
    published_at: str
    title: str
    view_count: int
    like_count: int
    comment_count: int
    favorite_count: int
    duration: str
    comments: List[Comment]

    def to_dict(self):
        return {
            "topic": self.topic,
            "description": self.description,
            "title": self.title,
            "published_at": self.published_at,
            "view_count": self.view_count,
            "like_count": self.like_count,
            "comment_count": self.comment_count,
            "favorite_count": self.favorite_count,
            "duration": self.duration,
            "comments": [comment.to_dict() for comment in self.comments],
        }


class VideosRepository(ABC):
    @abstractmethod
    def add_videos(self, videos: List[Video]) -> bool:
        pass
