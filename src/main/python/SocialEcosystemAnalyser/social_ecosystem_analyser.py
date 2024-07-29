import os
import sys
from time import sleep

from dotenv import load_dotenv

from .database.health.api_health_repository import ApiHealthRepository
from .database.topics.api_topics_repository import ApiTopicsRepository
from .database.videos.api_videos_repository import ApiVideosRepository
from .utils.get_topics import GetTopics
from .youtube.youtube_api import YoutubeAPI

if not load_dotenv():
    print("Failed to load .env file", file=sys.stderr)
    sys.exit(1)

YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")


def main():
    """Main program function"""
    while not ApiHealthRepository.check_health():
        print(
            "Database is not ready, waiting 10 seconds to retry...")
        sleep(10)

    youtube_api = YoutubeAPI(YOUTUBE_API_KEY)

    topics = GetTopics.get_topics()

    for t in topics:

        next_page_token = ""
        while next_page_token is not None:
            topic = ApiTopicsRepository.get_topic_by_name(t.name)
            print(f"Topic: {topic.name}")
            next_page_token, videos_data = youtube_api.get_videos_data(
                topic.name, topic.next_page_token)

            print(f"Next page token: {next_page_token}")
            if next_page_token is None:
                ApiTopicsRepository.set_topic_as_finished(topic)
            else:
                ApiTopicsRepository.save_next_page_token(
                    topic.name, next_page_token, topic.type)

            print(
                f"Adding {len(videos_data)} videos to the database...")
            status = ApiVideosRepository.add_videos(videos_data)
            if status:
                print("Videos added to the database")
            else:
                print(
                    "Failed to add one or more videos to the database")

        print(f"Finished topic, next_page_token: {next_page_token}")

    sys.exit(0)


if __name__ == "__main__":
    main()
