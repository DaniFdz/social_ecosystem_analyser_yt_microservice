import pytest

from src.main.python.SocialEcosystemAnalyser.database.videos.api_videos_repository import \
    ApiVideosRepository
from src.main.python.SocialEcosystemAnalyser.database.videos.videos_repository import (
    Comment, Video)


@pytest.mark.unittest
class TestVideo:
    def test_video_to_dict(self):
        """It should return a dictionary with the video data"""
        video = Video(
            id="00000",
            topic="Test",
            description="Test",
            title="Test",
            view_count=0,
            like_count=0,
            comment_count=0,
            favorite_count=0,
            duration="0:00",
            comments=[],
            published_at="2024-06-13T05:00:23Z",
        )
        assert video.to_dict() == {
            "id": "00000",
            "topic": "Test",
            "description": "Test",
            "title": "Test",
            "view_count": 0,
            "like_count": 0,
            "comment_count": 0,
            "favorite_count": 0,
            "duration": "0:00",
            "comments": [],
            "published_at": "2024-06-13T05:00:23Z",
        }


@pytest.mark.unittest
class TestComment:
    def test_comment_to_dict(self):
        """It should return a dictionary with the comment data"""
        comment = Comment(
            is_author=True,
            text="Test",
            like_count=0,
            published_at="2021-01-01",
        )
        assert comment.to_dict() == {
            "is_author": True,
            "text": "Test",
            "like_count": 0,
            "published_at": "2021-01-01",
        }


@pytest.mark.api
@pytest.mark.integration
class TestApiVideosRepository:
    def get_videos(self, mocker):
        """It should return a list of videos"""
        mocker.patch(
            "src.main.python.SocialEcosystemAnalyser.database.videos.api_videos_repository.r.get",
            return_value=type("Response", (object, ), {
                "status_code": 200,
                "json": lambda: []
            }),
        )
        assert ApiVideosRepository.get_videos()

    def test_get_videos_error(self, mocker):
        """It should return an empty list if the API returns an error"""
        mocker.patch(
            "src.main.python.SocialEcosystemAnalyser.database.videos.api_videos_repository.r.get",
            return_value=type("Response", (object, ), {"status_code": 500}),
        )
        assert ApiVideosRepository.get_videos() == []

    def test_add_videos(self, mocker):
        """It should return True if the videos are added"""
        videos = [
            Video(
                id="00000",
                topic="Test",
                description="Test",
                title="Test",
                view_count=0,
                like_count=0,
                comment_count=0,
                favorite_count=0,
                duration="0:00",
                comments=[],
                published_at="2024-06-13T05:00:23Z",
            )
        ]
        mocker.patch(
            "src.main.python.SocialEcosystemAnalyser.database.videos.api_videos_repository.r.post",
            return_value=type("Response", (object, ), {"status_code": 201}),
        )
        assert ApiVideosRepository.add_videos(videos)

    def test_add_videos_no_videos(self, mocker):
        """It should return False if no videos are added"""
        assert not ApiVideosRepository.add_videos([])

    def test_add_videos_error(self, mocker):
        """It should return False if the API returns an error"""
        videos = [
            Video(
                id="00000",
                topic="Test",
                description="Test",
                title="Test",
                view_count=0,
                like_count=0,
                comment_count=0,
                favorite_count=0,
                duration="0:00",
                comments=[],
                published_at="2024-06-13T05:00:23Z",
            )
        ]
        mocker.patch(
            "src.main.python.SocialEcosystemAnalyser.database.videos.api_videos_repository.r.post",
            return_value=type("Response", (object, ), {"status_code": 500}),
        )
        assert not ApiVideosRepository.add_videos(videos)
