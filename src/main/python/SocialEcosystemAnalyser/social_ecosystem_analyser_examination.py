import logging
import os
import sys
from time import sleep

from dotenv import load_dotenv

from .database.health.api_health_repository import ApiHealthRepository
# from .database.videos.api_videos_repository import ApiVideosRepository
from .settings import LOGGING
from .virustTotal.check_url import VTApi

if not load_dotenv():
    logging.error("Failed to load .env file")
    sys.exit(1)

VIRUSTOTAL_API_KEY = os.environ.get("VIRUSTOTAL_API_KEY")
logging.basicConfig(
    format=LOGGING["formatters"]["standard"]["format"])  # type: ignore


def main():
    """Main program function"""
    while not ApiHealthRepository.check_health():
        logging.warning(
            "Database is not ready, waiting 10 seconds to retry...")
        sleep(10)

    vt_api = VTApi(VIRUSTOTAL_API_KEY)
    _ = vt_api.get_url_report("https://www.youtube.com/")

    sys.exit(0)


if __name__ == "__main__":
    main()
