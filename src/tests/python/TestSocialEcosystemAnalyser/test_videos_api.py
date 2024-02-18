import pytest

from src.main.python.SocialEcosystemAnalyser.database.videos.api_videos_repository import \
    ApiVideosRepository
from src.main.python.SocialEcosystemAnalyser.database.videos.videos_repository import \
    Video


@pytest.mark.api
@pytest.mark.integration
class TestApiVideosRepository:
    def test_add_videos(self, mocker):
        """It should return True if the videos are added"""
        videos = [
            Video(
                topic="Test",
                description="Test",
                title="Test",
                view_count=0,
                like_count=0,
                comment_count=0,
                favorite_count=0,
                duration="0:00",
                comments=[],
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
                topic="Test",
                description="Test",
                title="Test",
                view_count=0,
                like_count=0,
                comment_count=0,
                favorite_count=0,
                duration="0:00",
                comments=[],
            )
        ]
        mocker.patch(
            "src.main.python.SocialEcosystemAnalyser.database.videos.api_videos_repository.r.post",
            return_value=type("Response", (object, ), {"status_code": 500}),
        )
        assert not ApiVideosRepository.add_videos(videos)
