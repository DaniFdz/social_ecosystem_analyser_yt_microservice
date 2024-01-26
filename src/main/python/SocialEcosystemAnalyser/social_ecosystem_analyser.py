import json
import os
import sys

from decouple import config
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from oauth2client.tools import run_flow

from .database_management import DatabaseManagement
from .nlp.similar_topics_generation import generate_topics
from .social_ecosystem_analyser_exception import (
    MessageExceptions, SocialEcosystemAnalyserException)
from .youtube.youtube_api import YoutubeAPI

YOUTUBE_API_KEY = config("YOUTUBE_API_KEY")
OAUTH_CLIENT_ID = config("OAUTH_CLIENT_ID")
OAUTH_CLIENT_SECRET = config("OAUTH_CLIENT_SECRET")
OAUTH_SCOPE = config("OAUTH_SCOPE")
OAUTH_REDIRECT_URI = config("OAUTH_REDIRECT_URI")
COHERE_API_KEY = config("COHERE_API_KEY")


def our_exit():
    """ Exit the program

        TODO: This function should be chaged entirely
    """
    db = DatabaseManagement()
    db.__del__()
    sys.exit()


def main():
    """ Main program function """
    if not os.path.exists("creds.data"):
        flow = OAuth2WebServerFlow(client_id=OAUTH_CLIENT_ID,
                                   client_secret=OAUTH_CLIENT_SECRET,
                                   scope=OAUTH_SCOPE,
                                   redirect_uri=OAUTH_REDIRECT_URI)
        storage = Storage("creds.data")
        oauth_token = run_flow(flow, storage).access_token
    else:
        oauth_token = json.load(open("creds.data", "r"))["access_token"]

    database_management = DatabaseManagement()
    youtube_api = YoutubeAPI(YOUTUBE_API_KEY, oauth_token)

    topic = input("Enter a topic: ")

    try:
        topics = generate_topics(topic, COHERE_API_KEY)
    except SocialEcosystemAnalyserException as e:
        print(e)
        if input("Do you want to continue? (Y/n): ").lower() == "n":
            our_exit()
        topics = [topic]

    print(f"[i] Testing topics: {topics}")

    i = 0
    while i < len(topics):
        try:
            next_page_token = database_management.get_next_page_token()
        except TypeError:
            next_page_token = None

        next_page_token, videos_data = youtube_api.get_videos_data(
            topics[i], next_page_token)

        if next_page_token is None:
            i += 1
            if database_management.delete_next_page_token() == 0:
                raise SocialEcosystemAnalyserException(
                    MessageExceptions.MONGO_DB_DELETE_ERROR)
        else:
            database_management.save_next_page_token(next_page_token)

        ids = database_management.add_videos(*videos_data)
        print(f"[i] Added {len(ids)} videos to the database")
        break

    our_exit()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        db = DatabaseManagement()
        db.__del__()
        raise e
