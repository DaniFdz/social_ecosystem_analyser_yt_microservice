from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class VTReport:
    first_submission_date: int
    last_modification_date: int
    last_http_response_content_length: int
    tags: List[str]
    html_meta: Dict[str, List[str]]
    times_submitted: int
    redirection_chain: List[str]
    trackers: Dict[str, List[Dict[str, str]]]
    threat_names: List[str]
    url: str
    domain: str
    categories: Dict[str, str]
    last_analysis_stats: Dict[str, int]
    reputation: int
    last_http_response_code: int
    last_http_response_headers: Dict[str, str]

    def __dict__(self) -> Dict:
        return {
            "first_submission_date": self.first_submission_date,
            "last_modification_date": self.last_modification_date,
            "last_http_response_content_length":
            self.last_http_response_content_length,
            "tags": self.tags,
            "html_meta": self.html_meta,
            "times_submitted": self.times_submitted,
            "redirection_chain": self.redirection_chain,
            "trackers": self.trackers,
            "threat_names": self.threat_names,
            "url": self.url,
            "domain": self.domain,
            "categories": self.categories,
            "last_analysis_stats": self.last_analysis_stats,
            "reputation": self.reputation,
            "last_http_response_code": self.last_http_response_code,
            "last_http_response_headers": self.last_http_response_headers,
        }


class VirustotalReportsRepository(ABC):
    @abstractmethod
    def get_virustotal_report_by_url(cls, url: str) -> bool:
        pass

    @abstractmethod
    def add_virustotal_reports(cls, reports: List[VTReport]) -> bool:
        pass
