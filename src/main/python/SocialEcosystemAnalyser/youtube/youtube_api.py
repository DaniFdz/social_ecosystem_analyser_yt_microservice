import icecream as ic  # type: ignore # noqa: F401
import requests as req
from langdetect import detect

from ..social_ecosystem_analyser_exception import (
    MessageExceptions, SocialEcosystemAnalyserException)


class YoutubeAPI:
    def __init__(self, api_key: str, version: str = "v3"):
        self.api_key = api_key
        self.base_url = f"https://www.googleapis.com/youtube/{version}/"

    def _videos_list_from_topic(
        self, search_query: str, next_page_token: str
    ):  # Q PERMITE USAR OPERACORES COMO NOT O OR OTRA OPCION ES HACER MULTIPLES REQUESTS Y LUEGO QUITAR REPETIDOS
        url = self.base_url + "search"
        params = {
            "key": self.api_key,
            "part": "id",
            "type": "video",
            "order": "title",
            "q": search_query,
            "maxResults": 50,
            "language": "en",
            "fields": "nextPageToken,items(id(videoId))"
        }

        if next_page_token is not None:
            params["pageToken"] = next_page_token

        res = req.get(url, params=params)
        if "error" in res.json():
            if res.json()["error"]["errors"][0]["reason"] == "quotaExceeded":
                raise SocialEcosystemAnalyserException(
                    MessageExceptions.YOUTUBE_API_QUOTA_EXCEEDED)
            elif "API key not valid" in res.json(
            )["error"]["errors"][0]["message"]:
                raise SocialEcosystemAnalyserException(
                    MessageExceptions.YOUTUBE_API_KEY_ERROR)
            else:
                raise SocialEcosystemAnalyserException(
                    MessageExceptions.YOUTUBE_API_ERROR)

        return res.json()

    def _video_list_stats(self, video_ids: list):
        url = self.base_url + "videos"
        params = {
            "key":
            self.api_key,
            "part":
            "statistics, contentDetails, snippet",
            "id":
            ",".join(video_ids),
            "fields":
            "items(statistics,contentDetails(duration),snippet(title,description,channelTitle,channelId))"
        }
        res = req.get(url, params=params)

        if "error" in res.json():
            if res.json()["error"]["errors"][0]["reason"] == "quotaExceeded":
                raise SocialEcosystemAnalyserException(
                    MessageExceptions.YOUTUBE_API_QUOTA_EXCEEDED)
            elif "API key not valid" in res.json(
            )["error"]["errors"][0]["message"]:
                raise SocialEcosystemAnalyserException(
                    MessageExceptions.YOUTUBE_API_KEY_ERROR)
            else:
                raise SocialEcosystemAnalyserException(
                    MessageExceptions.YOUTUBE_API_ERROR)

        return res.json()

    def _comments_list_from_video(self, search_query: str,
                                  next_page_token: str):
        url = self.base_url + "commentThreads"
        params = {
            "key":
            self.api_key,
            "part":
            "id,snippet",
            "videoId":
            search_query,
            "maxResults":
            100,
            "fields":
            "items(id,snippet(topLevelComment(snippet(authorDisplayName,authorChannelId,likeCount,publishedAt,textDisplay))))"  # type: ignore # noqa: E501
        }

        if next_page_token != "":
            params["pageToken"] = next_page_token

        res = req.get(url, params=params)

        if "error" in res.json():
            if "disabled comments" in res.json(
            )["error"]["errors"][0]["message"]:
                return []
            elif res.json()["error"]["errors"][0]["reason"] == "quotaExceeded":
                raise SocialEcosystemAnalyserException(
                    f'{MessageExceptions.YOUTUBE_API_QUOTA_EXCEEDED}: {res.json()["error"]["errors"][0]["message"]}'
                )
            elif "API key not valid" in res.json(
            )["error"]["errors"][0]["message"]:
                raise SocialEcosystemAnalyserException(
                    f'{MessageExceptions.YOUTUBE_API_KEY_ERROR}: {res.json()["error"]["errors"][0]["message"]}'
                )
            else:
                raise SocialEcosystemAnalyserException(
                    f'{MessageExceptions.YOUTUBE_API_ERROR}: {res.json()["error"]["errors"][0]["message"]}'
                )

        return list(
            map(
                lambda x: {
                    "authorId":
                    x["snippet"]["topLevelComment"]["snippet"][
                        "authorChannelId"]["value"],
                    "textDisplay":
                    x["snippet"]["topLevelComment"]["snippet"]["textDisplay"],
                    "likeCount":
                    x["snippet"]["topLevelComment"]["snippet"]["likeCount"]
                },
                res.json()["items"]))

    # ToDo: Need to implement OAuth2.0 to get subtitles
    # def _subtitles_from_video(self, search_query: str, next_page_token: str):
    #     url = self.base_url + "captions/list"
    #     params = {
    #         "key": self.api_key,
    #         "part": "id,snippet",
    #         "videoId": search_query,
    #         "maxResults": 100,
    #         "fields": "nextPageToken,items(id,snippet(text))"
    #     }

    #     if next_page_token is not None:
    #         params["pageToken"] = next_page_token

    #     res = req.get(url, params=params)

    #     if "error" in res.json():
    #         if res.json()["error"]["errors"][0]["reason"] == "quotaExceeded":
    #             raise SocialEcosystemAnalyserException(
    #                 f"{MessageExceptions.YOUTUBE_API_QUOTA_EXCEEDED}: {res.json()["error"]["errors"][0]["message"]}"
    #             )
    #         elif "API key not valid" in res.json()["error"]["errors"][0]["message"]:
    #             raise SocialEcosystemAnalyserException(
    #                 f"{MessageExceptions.YOUTUBE_API_KEY_ERROR}: {res.json()["error"]["errors"][0]["message"]}"
    #             )
    #         else:
    #             raise SocialEcosystemAnalyserException(
    #                 f"{MessageExceptions.YOUTUBE_API_ERROR}: {res.json()["error"]["errors"][0]["message"]}"
    #             )

    #     return res.json()

    def get_videos_data(self, search_query: str, next_page_token: str):
        videos = self._videos_list_from_topic(search_query, next_page_token)

        video_ids = [video["id"]["videoId"] for video in videos["items"]]
        videos_stats = self._video_list_stats(video_ids)

        indexes = []
        for i in range(len(videos_stats["items"])):
            description = videos_stats["items"][i]["snippet"]["description"]
            title = videos_stats["items"][i]["snippet"]["title"]
            if description != "":
                if detect(description) == "en":
                    indexes.append(i)
            elif title != "":
                if detect(title) == "en":
                    indexes.append(i)

        video_ids = [video_ids[i] for i in indexes]
        videos_stats = [videos_stats["items"][i] for i in indexes]

        comments = []
        # subtitles = []
        for video_id in video_ids:
            comments.append(self._comments_list_from_video(video_id, ""))
            # subtitles.append(self._subtitles_from_video(video_id, ""))

        videos_data = []
        for i, video_id in enumerate(video_ids):
            try:
                videos_data.append({
                    "topic":
                    search_query,
                    "video_id":
                    video_id,
                    "channelId":
                    videos_stats[i]["snippet"]["channelId"],
                    "description":
                    videos_stats[i]["snippet"]["description"],
                    "title":
                    videos_stats[i]["snippet"]["title"],
                    "viewCount":
                    int(videos_stats[i]["statistics"]["viewCount"]),
                    "likeCount":
                    int(videos_stats[i]["statistics"]["likeCount"]),
                    "commentCount":
                    int(videos_stats[i]["statistics"]["commentCount"]),
                    "favoriteCount":
                    int(videos_stats[i]["statistics"]["favoriteCount"]),
                    "duration":
                    videos_stats[i]["contentDetails"]["duration"],
                    "comments":
                    comments[i],
                    # "subtitles": subtitles[i],
                })
            except KeyError:
                continue

        if "nextPageToken" not in videos:
            return None, videos_data

        return videos["nextPageToken"], videos_data
