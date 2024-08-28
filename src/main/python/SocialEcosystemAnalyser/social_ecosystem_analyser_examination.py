import os
import sys
from time import sleep, time

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

VIRUSTOTAL_API_KEY = os.environ.get("VIRUSTOTAL_API_KEY2")


def main():
    """Main program function"""
    while not ApiHealthRepository.check_health():
        print("Database is not ready, waiting 10 seconds to retry...")
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

    start_page_number = page_number
    start_global_time = time()
    vt_times = []
    video_times = []

    try:
        while 1:

            print(f"\033[;35mReport from page: {page_number}\033[0;m")

            videos = ApiVideosRepository.get_videos(page_number, 5)
            if not videos:
                break
            for video in videos:
                start_video_time = time()
                report = GeneralReport(
                    id=video.id,
                    topic=video.topic,
                    title=video.title,
                    description=video.description,
                    avg_score=(
                        video.score
                        if len(video.comments) == 0
                        else 0.3 * video.score
                        + 0.7 * sum(x.score for x in video.comments) / len(video.comments)
                    ),
                    view_count=video.view_count,
                    like_count=video.like_count,
                    published_at=video.published_at,
                    urls_reports=[],
                )
                print(f"Calculating report for video - {video.id}")

                for url in DetectUrl.detect_urls(video):
                    virustotal_report = ApiVirusTotalReportsRepository.get_virustotal_report_by_url(url)

                    if not virustotal_report:
                        start_vt_time = time()
                        url_id = vt_api.get_url_id(url)
                        if url_id is None:
                            continue
                        else:
                            url_id = url_id["data"]["id"].split("-")[1]

                        virustotal_report = vt_api.get_url_report(url_id)

                        elapsed_vt_time = time() - start_vt_time
                        vt_times.append(elapsed_vt_time)

                        if virustotal_report is None:
                            continue

                        ApiVirusTotalReportsRepository.add_virustotal_report(
                            virustotal_report
                        )

                    report.urls_reports.append(virustotal_report)

                if not ApiGeneralReportsRepository.add_general_report(report):
                    print("\033[;33mReport is already in the database\033[0;m")
                else:
                    print(f"\033[;32mReport for video - {video.id} added to the database\033[0;m")

                elapsed_video_time = time() - start_video_time
                video_times.append(elapsed_video_time)
                sleep(5)

            page_number += 1
            with open(f"{LOGS_FOLDER}/page_number.txt", "w") as file:
                file.write(str(page_number))

    except Exception as e:
        elapsed_global_time = time() - start_global_time
        print("\033[;36mElapsed global time: %.10f seconds.\033[0;m" % elapsed_global_time)
        print("\033[;36mAverage time for virustotal report: %.10f seconds.\033[0;m" % (sum(vt_times)/len(vt_times) if len(vt_times) > 0 else 0))
        print("\033[;36mNumber of virustotal reports: %d\033[0;m" % len(vt_times))
        print("\033[;36mAverage time for video: %.10f seconds.\033[0;m" % (sum(video_times)/len(video_times) if len(video_times) > 0 else 0))
        print(f"\033[;36mFinished page: {start_page_number} - {page_number}, a total of {(page_number - start_page_number)*5} videos\033[0;m")

if __name__ == "__main__":
    main()
