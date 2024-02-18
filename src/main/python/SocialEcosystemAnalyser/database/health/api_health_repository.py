import os

import requests as r

from .health_repository import HealthRepository


class ApiHealthRepository(HealthRepository):
    __api = os.environ.get("API_URL")
    __endpoint = "health/"
    __token = os.environ.get("API_TOKEN")

    @classmethod
    def check_health(cls):
        """
        Fetches GET health/

        @return: bool: If the API is healthy
        """
        endpoint = cls.__api + "health/"
        try:
            res = r.get(endpoint)
        except r.exceptions.ConnectionError:
            return False

        return res.status_code == 200