import os
import sys

from dotenv import load_dotenv

from .database_management import DatabaseManagement
from .exceptions.social_ecosystem_analyser_exception import (
    MessageExceptions, SocialEcosystemAnalyserException)
from .nlp.similar_topics_generation import generate_topics
from .youtube.youtube_api import YoutubeAPI

load_dotenv()
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")
COHERE_API_KEY = os.environ.get("COHERE_API_KEY")


def our_exit():
    """ Exit the program"""
    db = DatabaseManagement()
    db.__del__()
    sys.exit()


def main():
    """ Main program function """
    database_management = DatabaseManagement()
    youtube_api = YoutubeAPI(YOUTUBE_API_KEY)

    if not os.path.exists("topics.txt"):
        print("[!] File topics.txt not found")
        our_exit()

    with open("topics.txt", "r") as file:
        topics = file.readlines()

    if len(topics) == 0:
        print("[!] No topics found in topics.txt")
        our_exit()

    topic = topics[0].strip()
    print(f"[i] Topic: {topic}")

    with open("topics.txt", "w") as file:
        file.writelines(topics[1:])

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
