import pytest
from requests import exceptions

from src.main.python.SocialEcosystemAnalyser.database.health.api_health_repository import \
    ApiHealthRepository


@pytest.mark.api
@pytest.mark.integration
class TestApiHealthRepository:
    def test_check_health(self, mocker):
        """It should return True if the API is up"""
        mocker.patch(
            "src.main.python.SocialEcosystemAnalyser.database.health.api_health_repository.r.get",
            return_value=type("Response", (object, ), {"status_code": 200}),
        )
        assert ApiHealthRepository.check_health()

    def test_check_health_server_down(self, mocker):
        """It should return False if the API is down"""
        mocker.patch(
            "src.main.python.SocialEcosystemAnalyser.database.health.api_health_repository.r.get",
            side_effect=exceptions.ConnectionError,
        )
        assert not ApiHealthRepository.check_health()

    def test_check_health_server_error(self, mocker):
        """It should return False if the API returns an error"""
        mocker.patch(
            "src.main.python.SocialEcosystemAnalyser.database.health.api_health_repository.r.get",
            return_value=type("Response", (object, ), {"status_code": 500}),
        )
        assert not ApiHealthRepository.check_health()
