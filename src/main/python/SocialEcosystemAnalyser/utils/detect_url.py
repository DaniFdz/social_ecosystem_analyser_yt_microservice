import logging
import re
from typing import Set

from src.main.python.SocialEcosystemAnalyser.database.videos.videos_repository import \
    Video
from src.main.python.SocialEcosystemAnalyser.settings import LOGGING

logging.basicConfig(format=LOGGING["formatters"]["standard"]["format"])


class DetectUrl:
    @classmethod
    def detect_urls(cls, video: Video) -> Set[str]:
        """
        Detect urls in the video description and comments

        @param: video: Video

        @return: Set[string] List of urls
        """
        urls = cls.detect_url_in_string(video.description)
        for comment in video.comments:
            urls = urls.union(cls.detect_url_in_string(str(comment.text)))
        return urls

    @staticmethod
    def detect_url_in_string(string: str) -> Set[str]:
        """
        Detect urls inside of a string

        @param string: str -> String to detect urls from
        @return Set[str] -> List of urls inside the string
        """
        return set(
            re.findall("(?P<url>http[s]{0,1}://[\\da-zA-Z./\\-?&=_]+)",
                       string))
