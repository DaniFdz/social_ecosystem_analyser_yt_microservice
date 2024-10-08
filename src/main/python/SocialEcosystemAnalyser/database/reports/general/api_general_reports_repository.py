import requests as r

from src.main.python.SocialEcosystemAnalyser.database.api_repository.api_repository import \
    ApiRepository
from src.main.python.SocialEcosystemAnalyser.database.reports.general.general_reports_repository import (
    GeneralReport, GeneralReportsRepository)


class ApiGeneralReportsRepository(GeneralReportsRepository, ApiRepository):
    __endpoint = "api/v1/reports/"

    @classmethod
    def get_general_report_by_url(cls, url: str) -> bool:
        """
        Fetches Get /api/v1/general/:url

        @return: bool: If report exists
        """
        endpoint = cls._api + cls.__endpoint + "/" + url
        res = r.get(endpoint,
                    headers={"Authorization": f"Bearer {cls._token}"})

        return res.status_code == 200

    @classmethod
    def add_general_report(cls, report: GeneralReport) -> bool:
        """
        Fetches Post /api/v1/general/

        @return: bool: If report was created
        """
        if report is None:
            return False
        endpoint = cls._api + cls.__endpoint
        res = r.post(
            endpoint,
            headers={"Authorization": f"Bearer {cls._token}"},
            json=report.__dict__(),
        )
        return res.status_code == 201
