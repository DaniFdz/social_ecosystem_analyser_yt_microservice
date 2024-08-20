import requests as r

from src.main.python.SocialEcosystemAnalyser.database.api_repository.api_repository import \
    ApiRepository
from src.main.python.SocialEcosystemAnalyser.database.reports.virustotal.virustotal_reports_repository import (
    VirustotalReportsRepository, VTReport)


class ApiVirusTotalReportsRepository(VirustotalReportsRepository,
                                     ApiRepository):
    __endpoint = "api/v1/virustotal/"

    @classmethod
    def get_virustotal_report_by_url(cls, url: str) -> bool:
        """
        Fetches Get /api/v1/virustotal/url?url=""

        @return: bool: If report exists
        """
        endpoint = cls._api + cls.__endpoint + "/url"
        res = r.get(endpoint,
                    params={"url": url},
                    headers={"Authorization": f"Bearer {cls._token}"})

        if res.status_code != 200:
            return None
        data = res.json()
        return VTReport(
            data["first_submission_date"]
            if "first_submission_date" in data else 0,
            data["last_modification_date"]
            if "last_modification_date" in data else 0,
            (data["last_http_response_content_length"]
             if "last_http_response_content_length" in data else 0),
            data["tags"] if "tags" in data else [],
            data["html_meta"] if "html_meta" in data else dict(),
            data["times_submitted"] if "times_submitted" in data else 0,
            data["redirection_chain"] if "redirection_chain" in data else [],
            data["trackers"] if "trackers" in data else dict(),
            data["threat_names"] if "threat_names" in data else [],
            data["url"] if "url" in data else url,
            data["domain"] if "domain" in data else "",
            data["categories"] if "categories" in data else dict(),
            data["last_analysis_stats"]
            if "last_analysis_stats" in data else dict(),
            data["reputation"] if "reputation" in data else 0,
            data["last_http_response_code"]
            if "last_http_response_code" in data else 0,
            (data["last_http_response_headers"]
             if "last_http_response_headers" in data else dict()),
        )


    @classmethod
    def add_virustotal_report(cls, report: VTReport) -> bool:
        """
        Fetches Post /api/v1/virustotal/

        @return: bool: If report was created
        """
        if report is None:
            return False
        endpoint = cls._api + cls.__endpoint
        res = r.post(
            endpoint,
            headers={"Authorization": f"Bearer {cls._token}"},
            json=report.to_dict(),
        )
        return res.status_code == 201
