import os
import sys
from time import sleep, time

from dotenv import load_dotenv

from .database.health.api_health_repository import ApiHealthRepository
from .database.topics.api_topics_repository import ApiTopicsRepository
from .database.videos.api_videos_repository import ApiVideosRepository
from .utils.get_topics import GetTopics
from .youtube.youtube_api import YoutubeAPI

if not load_dotenv():
    print("Failed to load .env file", file=sys.stderr)
    sys.exit(1)

YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY2")


def main():
    """Main program function"""
    total_time = time()
    total_videos = 0


    while not ApiHealthRepository.check_health():
        print("Database is not ready, waiting 10 seconds to retry...")
        sleep(10)

    print("Conected to database")

    youtube_api = YoutubeAPI(YOUTUBE_API_KEY)

    try:
        topics = GetTopics.get_topics()

        for t in topics:
            next_page_token = ""
            while next_page_token is not None:
                topic = ApiTopicsRepository.get_topic_by_name(t.name)
                print(f"\033[;35mTopic: {topic.name}\033[0;m")

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

                total_videos += len(videos_data)

                if status:
                    print("\033[;32mVideos added to the database\033[0;m")
                else:
                    print("\033[;33mFailed to add one or more videos to the database\033[0;m")

            print(f"Finished topic{topic}, next_page_token: {next_page_token}")

    except Exception as e:
        elapsed_total_time = time() - total_time
        print(f"\033[;31mError: {e}\033[0;m")

        print(f"\033[;36mTotal elapsed time: {elapsed_total_time} seconds\033[0;m")
        print(f"\033[;36mTotal videos data collection: {total_videos}\033[0;m")
        print(f"\033[;36mAverage time per video: {elapsed_total_time / total_videos if total_videos > 0 else 0}\033[0;m")


        sys.exit(1)

if __name__ == "__main__":
    main()
