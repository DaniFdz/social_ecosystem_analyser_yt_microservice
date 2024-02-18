import os
from typing import List

import requests as r

from .videos_repository import Video, VideosRepository


class ApiVideosRepository(VideosRepository):
    __api = os.environ.get("API_URL")
    __endpoint = "api/v1/videos/"
    __token = os.environ.get("API_TOKEN")

    @classmethod
    def add_videos(cls, videos: List[Video]) -> bool:
        if len(videos) == 0:
            return False

        headers = {"Authorization": f"Bearer {cls.__token}"}
        response = r.post(
            f"{cls.__api}/{cls.__endpoint}",
            json=[video.to_dict() for video in videos],
            headers=headers,
        )

        return response.status_code == 201
