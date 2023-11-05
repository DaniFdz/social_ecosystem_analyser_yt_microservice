import os

from decouple import config

from .youtube.youtube_api import YoutubeAPI
from .database_management import DatabaseManagement
from .social_ecosystem_analyser_exception import SocialEcosystemAnalyserException, MessageExceptions
import icecream as ic

YOUTUBE_API_KEY = config('YOUTUBE_API_KEY')

def main():
    """ Main program function """
    database_management = DatabaseManagement()
    youtube_api = YoutubeAPI(YOUTUBE_API_KEY)

    try:
        x = True
        while x:
            try:
                next_page_token = database_management.get_next_page_token()
            except TypeError:
                next_page_token = None
            
            next_page_token, videos_data = youtube_api.get_videos_data("gaming", next_page_token)

            database_management.save_next_page_token(next_page_token)

            ids = database_management.add_videos(*videos_data)
            print(f"[i] Added {len(ids)} videos to the database")
            x = False

    except SocialEcosystemAnalyserException as e:
        print(e)
        os.kill(os.getpid(), 9)

if __name__ == "__main__":
    main()
    os.kill(os.getpid(), 9)