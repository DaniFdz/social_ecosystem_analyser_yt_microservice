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
            "part": "snippet",
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


        """
        # -*- coding: utf-8 -*-

        # Sample Python code for youtube.search.list
        # See instructions for running these code samples locally:
        # https://developers.google.com/explorer-help/code-samples#python

        import os

        import google_auth_oauthlib.flow
        import googleapiclient.discovery
        import googleapiclient.errors

        scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

        def main():
            # Disable OAuthlib's HTTPS verification when running locally.
            # *DO NOT* leave this option enabled in production.
            os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

            api_service_name = "youtube"
            api_version = "v3"
            client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"

            # Get credentials and create an API client
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                client_secrets_file, scopes)
            credentials = flow.run_console()
            youtube = googleapiclient.discovery.build(
                api_service_name, api_version, credentials=credentials)

            request = youtube.search().list(
                part="snippet",
                order="title",
                q="videojuego",
                type="video"
            )
            response = request.execute()

            print(response)

        if __name__ == "__main__":
            main()


        SOLUCION:

        {
  "kind": "youtube#searchListResponse",
  "etag": "BFiQtT6xWcroJ5tWJ1lP5u5BBic",
  "nextPageToken": "CAUQAA",
  "regionCode": "ES",
  "pageInfo": {
    "totalResults": 1000000,
    "resultsPerPage": 5
  },
  "items": [
    {
      "kind": "youtube#searchResult",
      "etag": "hT46DpuML8fTWQKN9OkSm4LJ6i0",
      "id": {
        "kind": "youtube#video",
        "videoId": "kamA4bjVVpE"
      },
      "snippet": {
        "publishedAt": "2022-10-10T22:29:27Z",
        "channelId": "UCvsBR3yVOg_KD-4tUqqK5dQ",
        "title": "1°mob a votar &quot;el oledor&quot; #videojuego #minecraft #shorts #minecraftmobvote #mob #plant",
        "description": "",
        "thumbnails": {
          "default": {
            "url": "https://i.ytimg.com/vi/kamA4bjVVpE/default.jpg",
            "width": 120,
            "height": 90
          },
          "medium": {
            "url": "https://i.ytimg.com/vi/kamA4bjVVpE/mqdefault.jpg",
            "width": 320,
            "height": 180
          },
          "high": {
            "url": "https://i.ytimg.com/vi/kamA4bjVVpE/hqdefault.jpg",
            "width": 480,
            "height": 360
          }
        },
        "channelTitle": "BLAKI DOG",
        "liveBroadcastContent": "none",
        "publishTime": "2022-10-10T22:29:27Z"
      }
    },
    {
      "kind": "youtube#searchResult",
      "etag": "_HlXCTYtipPgrRPmxTTlpaHCSg4",
      "id": {
        "kind": "youtube#video",
        "videoId": "XN0Wp3Hw400"
      },
      "snippet": {
        "publishedAt": "2023-09-28T16:00:22Z",
        "channelId": "UClNSdNAqetoA97IG9zvscow",
        "title": "10 MODOS DE JUEGO que son MÁS ADICTIVOS que LA HISTORIA PRINCIPAL",
        "description": "Juegos y Tarjetas Prepago Más Baratas: https://www.eneba.com/es/?af_id=caverna Descarga la APP de Eneba y obtén ...",
        "thumbnails": {
          "default": {
            "url": "https://i.ytimg.com/vi/XN0Wp3Hw400/default.jpg",
            "width": 120,
            "height": 90
          },
          "medium": {
            "url": "https://i.ytimg.com/vi/XN0Wp3Hw400/mqdefault.jpg",
            "width": 320,
            "height": 180
          },
          "high": {
            "url": "https://i.ytimg.com/vi/XN0Wp3Hw400/hqdefault.jpg",
            "width": 480,
            "height": 360
          }
        },
        "channelTitle": "La Caverna del Gamer",
        "liveBroadcastContent": "none",
        "publishTime": "2023-09-28T16:00:22Z"
      }
    },
    {
      "kind": "youtube#searchResult",
      "etag": "E0GCe2gja9_eNkeoRj0_Z0RwITU",
      "id": {
        "kind": "youtube#video",
        "videoId": "ou9tTWqFZ_M"
      },
      "snippet": {
        "publishedAt": "2022-11-01T22:54:18Z",
        "channelId": "UC4BtoPpW5BkTO4J21-KAgsg",
        "title": "10 VIDEOJUEGOS que son OBRAS MAESTRAS 😍🤯 #videojuegos #shorts",
        "description": "Sígueme en INSTAGRAM: https://www.instagram.com/soythalas/",
        "thumbnails": {
          "default": {
            "url": "https://i.ytimg.com/vi/ou9tTWqFZ_M/default.jpg",
            "width": 120,
            "height": 90
          },
          "medium": {
            "url": "https://i.ytimg.com/vi/ou9tTWqFZ_M/mqdefault.jpg",
            "width": 320,
            "height": 180
          },
          "high": {
            "url": "https://i.ytimg.com/vi/ou9tTWqFZ_M/hqdefault.jpg",
            "width": 480,
            "height": 360
          }
        },
        "channelTitle": "Soy Thalas",
        "liveBroadcastContent": "none",
        "publishTime": "2022-11-01T22:54:18Z"
      }
    },
    {
      "kind": "youtube#searchResult",
      "etag": "Lw_1ots4pYQGYoNl8uCIxhCu2OU",
      "id": {
        "kind": "youtube#video",
        "videoId": "0pf0t0BrVuE"
      },
      "snippet": {
        "publishedAt": "2023-09-27T16:00:02Z",
        "channelId": "UClNSdNAqetoA97IG9zvscow",
        "title": "10 VIDEOJUEGOS que SON TREMENDAMENTE HOSTILES con EL JUGADOR",
        "description": "Juegos y Tarjetas Prepago Más Baratas: https://www.eneba.com/es/?af_id=caverna Descarga la APP de Eneba y obtén ...",
        "thumbnails": {
          "default": {
            "url": "https://i.ytimg.com/vi/0pf0t0BrVuE/default.jpg",
            "width": 120,
            "height": 90
          },
          "medium": {
            "url": "https://i.ytimg.com/vi/0pf0t0BrVuE/mqdefault.jpg",
            "width": 320,
            "height": 180
          },
          "high": {
            "url": "https://i.ytimg.com/vi/0pf0t0BrVuE/hqdefault.jpg",
            "width": 480,
            "height": 360
          }
        },
        "channelTitle": "La Caverna del Gamer",
        "liveBroadcastContent": "none",
        "publishTime": "2023-09-27T16:00:02Z"
      }
    },
    {
      "kind": "youtube#searchResult",
      "etag": "60a0OflVIzLLXVthKSSv36BMEqI",
      "id": {
        "kind": "youtube#video",
        "videoId": "b12gOP0ufdU"
      },
      "snippet": {
        "publishedAt": "2023-09-28T16:56:56Z",
        "channelId": "UCiQDnovgDtqtq_wh69s9y8A",
        "title": "10 Videojuegos Que Tuvieron una EXTRAÑA OBSESION Con Las PECHUGOTAS",
        "description": "Regresamos con otro conteo y en esta ocasión estamos hablando de las 10 Videojuegos Que Tuvieron una EXTRAÑA ...",
        "thumbnails": {
          "default": {
            "url": "https://i.ytimg.com/vi/b12gOP0ufdU/default.jpg",
            "width": 120,
            "height": 90
          },
          "medium": {
            "url": "https://i.ytimg.com/vi/b12gOP0ufdU/mqdefault.jpg",
            "width": 320,
            "height": 180
          },
          "high": {
            "url": "https://i.ytimg.com/vi/b12gOP0ufdU/hqdefault.jpg",
            "width": 480,
            "height": 360
          }
        },
        "channelTitle": "JuegaMela",
        "liveBroadcastContent": "none",
        "publishTime": "2023-09-28T16:56:56Z"
      }
    }
  ]
}

        """