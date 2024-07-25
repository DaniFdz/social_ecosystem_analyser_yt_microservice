from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Comment:
    is_author: bool
    text: str
    score: float
    like_count: int
    published_at: str

    def to_dict(self):
        return {
            "is_author": self.is_author,
            "text": self.text,
            "score": self.score,
            "like_count": self.like_count,
            "published_at": self.published_at,
        }


@dataclass
class Video:
    id: str
    topic: str
    description: str
    score: float
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
            "id": self.id,
            "topic": self.topic,
            "description": self.description,
            "title": self.title,
            "score": self.score,
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
    def get_videos(cls, page_number: Optional[int] = None) -> List[Video]:
        pass

    @abstractmethod
    def add_videos(self, videos: List[Video]) -> bool:
        pass
