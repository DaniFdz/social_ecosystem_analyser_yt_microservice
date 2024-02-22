import os
from typing import List

import requests as r
from dotenv import load_dotenv

from .videos_repository import Video, VideosRepository


class ApiVideosRepository(VideosRepository):
    load_dotenv()
    __api = os.environ.get("API_URL")
    __endpoint = "api/v1/videos/"
    __token = os.environ.get("API_TOKEN")

    @classmethod
    def add_videos(cls, videos: List[Video]) -> bool:
        if len(videos) == 0:
            return False

        headers = {"Authorization": f"Bearer {cls.__token}"}
        for video in videos:
            print(video.to_dict())
            response = r.post(
                f"{cls.__api}/{cls.__endpoint}",
                data=video.to_dict(),
                headers=headers,
            )
            if response.status_code != 201:
                return False

        return True
