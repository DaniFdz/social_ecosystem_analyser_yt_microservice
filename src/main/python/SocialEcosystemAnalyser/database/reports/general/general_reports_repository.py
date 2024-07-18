from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class URLReport:
    redirection_chain: List[str]
    categories: Dict[str, str]
    last_analysis_stats: Dict[str, int]
    reputation: int
    result: int

    def to_dict(self):
        return {
            "redirection_chain": self.redirection_chain,
            "categories": self.categories if self.categories else {},
            "last_analysis_stats": self.last_analysis_stats,
            "reputation": self.reputation,
            "result": self.result
        }


@dataclass
class GeneralReport:
    id: str
    topic: str
    title: str
    description: str
    avg_score: float
    view_count: int
    like_count: int
    published_at: str
    urls_reports: List[URLReport]

    def __dict__(self) -> Dict:
        return {
            "id":
            self.id,
            "topic":
            self.topic,
            "title":
            self.title,
            "description":
            self.description,
            "avg_score":
            self.avg_score,
            "published_at":
            self.published_at,
            "view_count":
            self.view_count,
            "like_count":
            self.like_count,
            "urls_reports":
            [url_report.to_dict() for url_report in self.urls_reports]
        }


class GeneralReportsRepository(ABC):
    @abstractmethod
    def get_general_report_by_url(cls, url: str) -> bool:
        pass

    @abstractmethod
    def add_general_report(cls, reports: List[GeneralReport]) -> bool:
        pass
