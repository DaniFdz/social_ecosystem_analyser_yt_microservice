import logging
import os
import sys
from time import sleep

from dotenv import load_dotenv

from main.python.SocialEcosystemAnalyser.database.reports.general.general_reports_repository import \
    GeneralReport

from .database.health.api_health_repository import ApiHealthRepository
from .database.reports.general.api_general_reports_repository import \
    ApiGeneralReportsRepository
from .database.reports.virustotal.api_virustotal_reports_repository import \
    ApiVirusTotalReportsRepository
from .database.videos.api_videos_repository import ApiVideosRepository
from .settings import LOGGING
from .utils.detect_url import DetectUrl
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

    LOGS_FOLDER = os.path.expanduser("~/.logs")

    if not os.path.exists(f"{LOGS_FOLDER}"):
        os.makedirs(f"{LOGS_FOLDER}")

    if not os.path.exists(f"{LOGS_FOLDER}/page_number.txt"):
        page_number = 0
    else:
        with open(f"{LOGS_FOLDER}/page_number.txt", "r") as file:
            page_number = int(file.read())

    while 1:
        logging.info(f"Report from page: {page_number}")

        videos = ApiVideosRepository.get_videos(page_number)

        for video in videos:
            video_info = ApiVideosRepository.get_video_by_url(video)
            report = GeneralReport(link=video,
                                   topic=video_info["topic"],
                                   title=video_info["title"],
                                   description=video_info["description"],
                                   view_count=video_info["view_count"],
                                   like_count=video_info["like_count"],
                                   published_at=video_info["published_at"],
                                   url_reports=[])

            url_list = DetectUrl.detect_urls(video)
            for url in url_list:
                url_id = vt_api.get_url_id(url)["data"]["id"].split("-")[1]
                if not ApiVirusTotalReportsRepository.get_virustotal_report_by_url(
                        url):
                    virustotal_report = vt_api.get_url_report(url_id)
                    ApiVirusTotalReportsRepository.add_virustotal_report(
                        virustotal_report)
                    logging.info(
                        f"Virustotal report added to the database: {url}")

                    #Genrate General Report
                    report.url_reports.append({
                        "redirection_chain":
                        virustotal_report["data"]["attributes"]
                        ["redirection_chain"],
                        "categories":
                        virustotal_report["data"]["attributes"]["categories"],
                        "last_analysis_stats":
                        virustotal_report["data"]["attributes"]
                        ["last_analysis_stats"],
                        "reputation":
                        virustotal_report["data"]["attributes"]["reputation"],
                        "result":
                        virustotal_report["data"]["attributes"]["result"]
                    })

            ApiGeneralReportsRepository.add_general_report(report)
            logging.info(f"General report added to the database: {video}")

        page_number += 1
        with open(f"{LOGS_FOLDER}/page_number.txt", "w") as file:
            file.write(str(page_number))


if __name__ == "__main__":
    main()
