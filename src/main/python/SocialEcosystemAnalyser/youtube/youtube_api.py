import requests as req
from ..social_ecosystem_analyser_exception \
    import SocialEcosystemAnalyserException, MessageExceptions

class YoutubeAPI:
    def __init__(self, api_key: str, version: str = "v3"):
        self.api_key = api_key
        self.base_url = f"https://www.googleapis.com/youtube/{version}/"

    def _videos_list_from_topic(self, search_query: str, next_page_token: str): #Q PERMITE USAR OPERACORES COMO NOT(-) O or(|), OTRA OPCION ES HACER MULTIPLES REQUESTS Y LUEGO QUITAR REPETIDOS
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
        if res.status_code != 200:
            SocialEcosystemAnalyserException(
                MessageExceptions.YOUTUBE_API_ERROR
            )

        return res.json()

    def _video_list_stats(self, video_ids: list):
        url = self.base_url + "videos"
        params = {
            "key": self.api_key,
            "part": "statistics, contentDetails, snippet",
            "id": ",".join(video_ids),
            "fields": "items(statistics,contentDetails(duration),snippet(title,description,channelTitle,channelId))"
        }
        res = req.get(url, params=params)
        if res.status_code != 200:
            SocialEcosystemAnalyserException(
                MessageExceptions.YOUTUBE_API_ERROR
            )

        return res.json()
    
    def get_videos_data(self, search_query: str, next_page_token: str):
        videos = self._videos_list_from_topic(search_query, next_page_token)
        

        video_ids = [video["id"]["videoId"] for video in videos["items"]]
        videos_stats = self._video_list_stats(video_ids)

        videos_data = []
        for i, id in enumerate(video_ids):
            try:
                videos_data.append({
                    "video_id": id,
                    "channelId": videos_stats["items"][i]["snippet"]["channelId"],
                    "description": videos_stats["items"][i]["snippet"]["description"],
                    "title": videos_stats["items"][i]["snippet"]["title"],
                    "viewCount": int(videos_stats["items"][i]["statistics"]["viewCount"]),
                    "likeCount": int(videos_stats["items"][i]["statistics"]["likeCount"]),
                    "commentCount": int(videos_stats["items"][i]["statistics"]["commentCount"]),
                    "favoriteCount": int(videos_stats["items"][i]["statistics"]["favoriteCount"]),
                    "duration": videos_stats["items"][i]["contentDetails"]["duration"],
                })
            except KeyError:
                continue

        return videos["nextPageToken"], videos_data
    