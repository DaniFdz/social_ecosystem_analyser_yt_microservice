import logging
import os
import sys
from time import sleep

from dotenv import load_dotenv

from .database.health.api_health_repository import ApiHealthRepository
from .database.topics.api_topics_repository import ApiTopicsRepository
from .database.videos.api_videos_repository import ApiVideosRepository
from .settings import LOGGING
from .utils.get_topics import GetTopics
from .youtube.youtube_api import YoutubeAPI

if not load_dotenv():
    logging.error("Failed to load .env file")
    sys.exit(1)

YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")
logging.basicConfig(
    format=LOGGING["formatters"]["standard"]["format"])  # type: ignore


def main():
    """Main program function"""
    while not ApiHealthRepository.check_health():
        logging.warning(
            "Database is not ready, waiting 10 seconds to retry...")
        sleep(10)

    youtube_api = YoutubeAPI(YOUTUBE_API_KEY)

    topics = GetTopics.get_topics()

    for topic_name in topics:
        next_page_token = ""
        while next_page_token is not None:
            topic = ApiTopicsRepository.get_topic_by_name(topic_name)
            next_page_token, videos_data = youtube_api.get_videos_data(
                topic.name, topic.next_page_token)

            if next_page_token is None:
                ApiTopicsRepository.set_topic_as_finished(topic.name)
                ApiTopicsRepository.save_next_page_token(topic.name, "")
            else:
                ApiTopicsRepository.save_next_page_token(
                    topic.name, next_page_token)

            status = ApiVideosRepository.add_videos(*videos_data)
            if status:
                logging.info(
                    f"Added {len(videos_data)} videos to the database")
            else:
                logging.error("Failed to add videos to the database")
            break

    sys.exit(0)


if __name__ == "__main__":
    main()
