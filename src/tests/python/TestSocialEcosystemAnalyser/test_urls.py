import pytest

from src.main.python.SocialEcosystemAnalyser.database.videos.videos_repository import (
    Comment, Video)
from src.main.python.SocialEcosystemAnalyser.utils.detect_url import DetectUrl


@pytest.mark.unittest
class TestUrls:
    def test_detect_single_url_in_string(self):
        string = '<a href="https://www.google.com">https://www.google.com</a>'
        assert DetectUrl.detect_url_in_string(string) == {
            "https://www.google.com"
        }

    def test_detect_multiple_urls_in_string(self):
        string = (
            '<a href="https://www.google.com">https://www.google.com</a>' +
            '<a href="https://www.youtube.com">https://www.youtube.com</a>'  # noqa
        )
        assert DetectUrl.detect_url_in_string(string) == {
            "https://www.google.com",
            "https://www.youtube.com",
        }

    def test_detect_no_urls_in_string(self):
        string = "This is a string with no urls"
        assert DetectUrl.detect_url_in_string(string) == set()

    def test_detect_no_urls_and_url_mixed_in_string(self):
        string = (
            'This is a string with urls <a href="https://www.google.com/123">https://www.google.com/123</a>'
            +
            ' and <a href="https://www.youtube.com/klsd?s=4">https://www.youtube.com/klsd?s=4</a>'  # noqa
        )
        assert DetectUrl.detect_url_in_string(string) == {
            "https://www.google.com/123",
            "https://www.youtube.com/klsd?s=4",
        }

    def test_detect_urls_in_video(self):
        video = Video(
            id="00000",
            topic="topic",
            description=
            "<a href='https://www.google.com'>https://www.google.com</a>",
            title="title",
            view_count=1,
            like_count=1,
            comment_count=1,
            favorite_count=1,
            duration="1:00",
            comments=[
                Comment(
                    is_author=True,
                    text=
                    "<a href='https://www.youtube.com'>https://www.youtube.com</a>",
                    like_count=1,
                    published_at="2024-06-13T05:00:23Z",
                ),
                Comment(
                    is_author=False,
                    text="This is a comment with no urls",
                    like_count=1,
                    published_at="2024-06-13T05:00:23Z",
                ),
            ],
            published_at="2024-06-13T05:00:23Z")
        assert DetectUrl.detect_urls(video) == {
            "https://www.google.com",
            "https://www.youtube.com",
        }
