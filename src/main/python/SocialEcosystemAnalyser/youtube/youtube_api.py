from typing import List, Optional, Tuple

import icecream as ic  # type: ignore # noqa: F401
import requests as req
from langdetect import detect

from src.main.python.SocialEcosystemAnalyser.database.videos.videos_repository import (
    Comment, Video)
from src.main.python.SocialEcosystemAnalyser.nlp.text_analysis_score import \
    TextAnalysisScore

from ..exceptions.social_ecosystem_analyser_exception import \
    SocialEcosystemAnalyserException
from ..exceptions.social_ecosystem_analyser_messages import MessageExceptions


class YoutubeAPI:
    def __init__(self, api_key: str, version: str = "v3"):
        self.api_key = api_key
        self.base_url = f"https://www.googleapis.com/youtube/{version}/"
        self.sentimental_analysis = TextAnalysisScore()

    def _videos_list_from_topic(self, search_query: str, next_page_token: str):
        url = self.base_url + "search"
        params = {
            "key": self.api_key,
            "part": "id",
            "type": "video",
            "order": "title",
            "q": search_query,
            "maxResults": 10,
            "language": "en",
            "fields": "nextPageToken,items(id(videoId))",
        }

        if next_page_token is not None:
            params["pageToken"] = next_page_token

        res = req.get(url, params=params)
        if "error" in res.json():
            if res.json()["error"]["errors"][0]["reason"] == "quotaExceeded":
                raise SocialEcosystemAnalyserException(
                    MessageExceptions.YOUTUBE_API_QUOTA_EXCEEDED
                )
            elif "API key not valid" in res.json()["error"]["errors"][0]["message"]:
                raise SocialEcosystemAnalyserException(
                    MessageExceptions.YOUTUBE_API_KEY_ERROR
                )
            else:
                raise SocialEcosystemAnalyserException(
                    MessageExceptions.YOUTUBE_API_ERROR
                )

        return res.json()

    def _video_list_stats(self, video_ids: list):
        url = self.base_url + "videos"
        params = {
            "key": self.api_key,
            "part": "statistics, contentDetails, snippet",
            "id": ",".join(video_ids),
            "fields": "items(id,statistics,contentDetails(duration),snippet(title,description,channelTitle,channelId,publishedAt))",
        }
        res = req.get(url, params=params)

        if "error" in res.json():
            if res.json()["error"]["errors"][0]["reason"] == "quotaExceeded":
                raise SocialEcosystemAnalyserException(
                    MessageExceptions.YOUTUBE_API_QUOTA_EXCEEDED
                )
            elif "API key not valid" in res.json()["error"]["errors"][0]["message"]:
                raise SocialEcosystemAnalyserException(
                    MessageExceptions.YOUTUBE_API_KEY_ERROR
                )
            else:
                raise SocialEcosystemAnalyserException(
                    MessageExceptions.YOUTUBE_API_ERROR
                )

        return res.json()

    def _comments_list_from_video(
        self, search_query: str, next_page_token: str, authorChannelId: str
    ) -> List[Comment]:
        url = self.base_url + "commentThreads"
        params = {
            "key": self.api_key,
            "part": "id,snippet",
            "videoId": search_query,
            "maxResults": 10,
            "fields": "items(id,snippet(topLevelComment(snippet(authorDisplayName,authorChannelId,likeCount,publishedAt,textDisplay))))",  # type: ignore # noqa: E501
        }

        if next_page_token != "":
            params["pageToken"] = next_page_token

        res = req.get(url, params=params)

        if "error" in res.json():
            if "disabled comments" in res.json()["error"]["errors"][0]["message"]:
                return []
            elif res.json()["error"]["errors"][0]["reason"] == "quotaExceeded":
                raise SocialEcosystemAnalyserException(
                    f'{MessageExceptions.YOUTUBE_API_QUOTA_EXCEEDED}: {res.json()["error"]["errors"][0]["message"]}'
                )
            elif "API key not valid" in res.json()["error"]["errors"][0]["message"]:
                raise SocialEcosystemAnalyserException(
                    f'{MessageExceptions.YOUTUBE_API_KEY_ERROR}: {res.json()["error"]["errors"][0]["message"]}'
                )
            elif (
                "insufficient permissions"
                in res.json()["error"]["errors"][0]["message"]
            ):
                return []
            else:
                raise SocialEcosystemAnalyserException(
                    f'{MessageExceptions.YOUTUBE_API_ERROR}: {res.json()["error"]["errors"][0]["message"]}'
                )

        data = []
        for x in res.json()["items"]:
            try:
                if (
                    "authorChannelId" in x["snippet"]["topLevelComment"]["snippet"]
                    and x["snippet"]["topLevelComment"]["snippet"]["textDisplay"] and detect(
                        x["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                    )
                    == "en"
                ):
                    data.append(
                        Comment(
                            is_author=x["snippet"]["topLevelComment"]["snippet"][
                                "authorChannelId"
                            ]["value"]
                            == authorChannelId,
                            text=x["snippet"]["topLevelComment"]["snippet"][
                                "textDisplay"
                            ],
                            score=self.sentimental_analysis.get_text_analysis_score(
                                x["snippet"]["topLevelComment"]["snippet"][
                                    "textDisplay"
                                ]
                            ),
                            like_count=x["snippet"]["topLevelComment"]["snippet"][
                                "likeCount"
                            ],
                            published_at=x["snippet"]["topLevelComment"]["snippet"][
                                "publishedAt"
                            ],
                        )
                    )

            except:
                continue

        return data

    def get_videos_data(  # noqa: C901
        self, search_query: str, next_page_token: str
    ) -> Tuple[Optional[str], List[Video]]:
        videos = self._videos_list_from_topic(search_query, next_page_token)

        video_ids = [video["id"]["videoId"] for video in videos["items"]]
        videos_stats = self._video_list_stats(video_ids)

        indexes = self._filter_english_videos(videos_stats)

        video_ids = [video_ids[i] for i in indexes]
        videos_stats = [videos_stats["items"][i] for i in indexes]

        print(f"VideoIds ({len(video_ids)}): {video_ids}")

        comments = []
        for i, video_id in enumerate(video_ids):
            comments.append(
                self._comments_list_from_video(
                    video_id, "", videos_stats[i]["snippet"]["channelId"]
                )
            )

        videos_data = []
        for i in range(len(video_ids)):
            try:
                videos_data.append(
                    Video(
                        id=videos_stats[i]["id"],
                        topic=search_query,
                        description=videos_stats[i]["snippet"]["description"],
                        title=videos_stats[i]["snippet"]["title"],
                        score=self.sentimental_analysis.get_text_analysis_score(
                            f'{videos_stats[i]["snippet"]["title"]} - {videos_stats[i]["snippet"]["description"]}'
                        ),
                        published_at=videos_stats[i]["snippet"]["publishedAt"],
                        view_count=int(videos_stats[i]["statistics"]["viewCount"]),
                        like_count=int(videos_stats[i]["statistics"]["likeCount"] if "likeCount" in videos_stats[i]["statistics"] else 0),
                        comment_count=int(
                            videos_stats[i]["statistics"]["commentCount"] if "commentCount" in videos_stats[i]["statistics"] else 0
                        ),
                        favorite_count=int(
                            videos_stats[i]["statistics"]["favoriteCount"]
                        ),
                        duration=videos_stats[i]["contentDetails"]["duration"],
                        comments=comments[i],
                    )
                )
            except KeyError as e:
                print(f'\033[;31mError: {videos_stats[i]["id"]} - {e}\033[0;m')
                continue

        if "nextPageToken" not in videos:
            return None, videos_data

        return videos["nextPageToken"], videos_data

    def _filter_english_videos(self, videos_stats):
        indexes = []
        for i in range(len(videos_stats["items"])):
            title = videos_stats["items"][i]["snippet"]["title"]
            description = videos_stats["items"][i]["snippet"]["description"]
            try:
                if detect(title) == "en" or detect(description) == "en":
                    indexes.append(i)
            except:
                continue

        return indexes
