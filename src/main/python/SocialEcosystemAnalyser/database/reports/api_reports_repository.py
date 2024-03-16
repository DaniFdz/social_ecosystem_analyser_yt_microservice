from typing import List

import requests as r

from src.main.python.SocialEcosystemAnalyser.database.api_repository.api_repository import \
    ApiRepository
from src.main.python.SocialEcosystemAnalyser.database.reports.reports_repository import (
    ReportsRepository, VTReport)


class ApiReportsRepository(ReportsRepository, ApiRepository):
    __endpoint = "api/v1/reports/"

    @classmethod
    def add_reports(cls, reports: List[VTReport]) -> bool:
        """
        Fetches Post /api/v1/reports/

        @return: bool: If report was created
        """
        if not reports:
            return False

        endpoint = cls._api + cls.__endpoint
        res = r.post(endpoint,
                     headers={"Authorization": f"Bearer {cls._token}"},
                     json=[r.__dict__() for r in reports])

        return res.status_code == 201
