import json
from typing import List, Optional

import requests as r

from src.main.python.SocialEcosystemAnalyser.database.api_repository.api_repository import \
    ApiRepository

from .videos_repository import Comment, Video, VideosRepository


class ApiVideosRepository(VideosRepository, ApiRepository):
    __endpoint = "api/v1/videos/"

    @classmethod
    def get_videos(cls, page_number: Optional[int] = None, page_size: Optional[int] = None) -> List[Video]:
        headers = {
            "Authorization": f"Bearer {cls._token}",
            "Content-Type": "application/json; charset=utf-8",
        }

        url = cls._api + cls.__endpoint
        if page_number is not None:
            url += f"?pageNum={page_number}"
        if page_size is not None:
            url += f"&pageSize={page_size}"
        response = r.get(
            url=url,
            headers=headers,
        )

        if response.status_code != 200:
            return []

        videos = response.json()
        return [
            Video(
                id=video["id"],
                topic=video["topic"],
                description=video["description"] if "description" in video else "None",
                score=video["score"],
                title=video["title"],
                view_count=video["view_count"],
                like_count=video["like_count"],
                comment_count=video["comment_count"],
                favorite_count=video["favorite_count"],
                duration=video["duration"],
                comments=(
                    [
                        Comment(
                            is_author=comment["is_author"],
                            text=comment["text"],
                            score=comment["score"],
                            like_count=comment["like_count"],
                            published_at=comment["published_at"],
                        )
                        for comment in video["comments"]
                    ]
                    if "comments" in video
                    else []
                ),
                published_at=video["published_at"],
            )
            for video in videos["data"]
        ]

    @classmethod
    def add_videos(cls, videos: List[Video]) -> bool:
        if len(videos) == 0:
            return False

        headers = {
            "Authorization": f"Bearer {cls._token}",
            "Content-Type": "application/json; charset=utf-8",
        }

        success = True
        for video in videos:
            video_json = json.dumps(video.to_dict())

            response = r.post(
                url=cls._api + cls.__endpoint,
                data=video_json,
                headers=headers,
            )
            if response.status_code != 201:
                success = False

        return success
