from typing import List

import requests as r

from src.main.python.SocialEcosystemAnalyser.database.api_repository.api_repository import \
    ApiRepository
from src.main.python.SocialEcosystemAnalyser.database.reports.virustotal_reports_repository import (
    VirustotalReportsRepository, VTReport)


class ApiVirusTotalReportsRepository(VirustotalReportsRepository,
                                     ApiRepository):
    __endpoint = "api/v1/virustotal/"

    @classmethod
    def get_virustotal_report_by_url(cls, url: str) -> bool:
        """
        Fetches Get /api/v1/virustotal/:url

        @return: bool: If report exists
        """
        endpoint = cls._api + cls.__endpoint + "/" + url
        res = r.get(endpoint,
                    headers={"Authorization": f"Bearer {cls._token}"})

        return res.status_code == 200

    @classmethod
    def add_virustotal_reports(cls, reports: List[VTReport]) -> bool:
        """
        Fetches Post /api/v1/virustotal/

        @return: bool: If report was created
        """
        if not reports:
            return False

        endpoint = cls._api + cls.__endpoint
        res = r.post(
            endpoint,
            headers={"Authorization": f"Bearer {cls._token}"},
            json=[r.__dict__() for r in reports],
        )

        return res.status_code == 201
