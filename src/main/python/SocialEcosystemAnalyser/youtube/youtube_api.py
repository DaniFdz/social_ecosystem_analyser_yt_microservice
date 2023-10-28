import requests as req
from ..social_ecosystem_analyser_exception \
    import SocialEcosystemAnalyserException, MessageExceptions

class YoutubeAPI:
    def __init__(self, api_key: str, version: str = "v3"):
        self.api_key = api_key
        self.base_url = f"https://www.googleapis.com/youtube/{version}/"

    def videos_list_from_topic(self, search_query: str): #Q PERMITE USAR OPERACORES COMO NOT(-) O or(|), OTRA OPCION ES HACER MULTIPLES REQUESTS Y LUEGO QUITAR REPETIDOS
        url = self.base_url + "search"
        params = {
            "key": self.api_key,
            "part": "id,snippet",
            "type": "video",
            "order": "title",
            "q": search_query,
            "maxResults": 50,
        }
        res = req.get(url, params=params)
        if res.status_code != 200:
            SocialEcosystemAnalyserException(
                MessageExceptions.YOUTUBE_API_ERROR
            )

        return res.json()
    