import os
import sys
from time import sleep

from dotenv import load_dotenv

from .database.health.api_health_repository import ApiHealthRepository
from .database.reports.general.api_general_reports_repository import \
    ApiGeneralReportsRepository
from .database.reports.general.general_reports_repository import GeneralReport
from .database.reports.virustotal.api_virustotal_reports_repository import \
    ApiVirusTotalReportsRepository
from .database.videos.api_videos_repository import ApiVideosRepository
from .utils.detect_url import DetectUrl
from .virustTotal.check_url import VTApi

if not load_dotenv():
    print("Failed to load .env file", file=sys.stderr)
    sys.exit(1)

VIRUSTOTAL_API_KEY = os.environ.get("VIRUSTOTAL_API_KEY")


def main():
    """Main program function"""
    while not ApiHealthRepository.check_health():
        print(
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
        print(f"Report from page: {page_number}")

        for video in ApiVideosRepository.get_videos(page_number):
            report = GeneralReport(
                id=video.id,
                topic=video.topic,
                title=video.title,
                description=video.description,
                avg_score=video.score
                if len(video.comments) == 0 else 0.3 * video.score +
                0.7 * sum(x.score
                          for x in video.comments) / len(video.comments),
                view_count=video.view_count,
                like_count=video.like_count,
                published_at=video.published_at,
                urls_reports=[],
            )
            print(f"Calculating report for: {video.id} -> {video.score}")

            for url in DetectUrl.detect_urls(video):
                print(url)
                url_id = vt_api.get_url_id(url)["data"]["id"].split("-")[1]
                virustotal_report = ApiVirusTotalReportsRepository.get_virustotal_report_by_url(
                    url)
                if not virustotal_report:

                    virustotal_report = vt_api.get_url_report(url_id)
                    if virustotal_report is None:
                        continue

                    ApiVirusTotalReportsRepository.add_virustotal_report(
                        virustotal_report)

                report.urls_reports.append(virustotal_report)

            print(report)
            if not ApiGeneralReportsRepository.add_general_report(report):
                print("Report not added")
            sleep(5)

        page_number += 1
        with open(f"{LOGS_FOLDER}/page_number.txt", "w") as file:
            file.write(str(page_number))


if __name__ == "__main__":
    main()
