import json
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

        headers = {
            "Authorization": f"Bearer {cls.__token}",
            "Content-Type": "application/json; charset=utf-8"
        }

        for video in videos:
            video_json = json.dumps(video.to_dict())

            response = r.post(
                url=cls.__api + cls.__endpoint,
                data=video_json,
                headers=headers,
            )
            if response.status_code != 201:
                return False

        return True
