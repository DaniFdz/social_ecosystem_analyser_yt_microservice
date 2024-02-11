import os

from dotenv import load_dotenv

from .database.database_management import DatabaseManagement
from .utils.exit_program import ExitProgram
from .utils.get_topics import GetTopics
from .youtube.youtube_api import YoutubeAPI

load_dotenv()
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")
COHERE_API_KEY = os.environ.get("COHERE_API_KEY")


def main():
    """ Main program function """
    database_management = DatabaseManagement()
    youtube_api = YoutubeAPI(YOUTUBE_API_KEY)

    topics = GetTopics.get_topics()

    for topic in topics:
        next_page_token = database_management.get_next_page_token(topic)

        next_page_token, videos_data = youtube_api.get_videos_data(
            topic, next_page_token)

        database_management.save_next_page_token(topics, next_page_token)

        ids = database_management.add_videos(*videos_data)
        print(f"[i] Added {len(ids)} videos to the database")
        break

    ExitProgram.exit_program()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        ExitProgram.exit_program(exception=e)
