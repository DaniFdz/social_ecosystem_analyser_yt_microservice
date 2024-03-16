import requests as r

from src.main.python.SocialEcosystemAnalyser.database.api_repository.api_repository import \
    ApiRepository

from .health_repository import HealthRepository


class ApiHealthRepository(HealthRepository, ApiRepository):
    __endpoint = "health/"

    @classmethod
    def check_health(cls):
        """
        Fetches GET health/

        @return: bool: If the API is healthy
        """
        endpoint = cls._api + cls.__endpoint
        try:
            res = r.get(endpoint)
        except r.exceptions.ConnectionError:
            return False

        return res.status_code == 200
