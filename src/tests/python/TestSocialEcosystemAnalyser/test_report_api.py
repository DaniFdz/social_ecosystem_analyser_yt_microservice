import pytest

from src.main.python.SocialEcosystemAnalyser.database.reports.general.api_general_reports_repository import \
    ApiGeneralReportsRepository
from src.main.python.SocialEcosystemAnalyser.database.reports.general.general_reports_repository import \
    GeneralReport


@pytest.mark.api
@pytest.mark.unittest
class TestReport:
    def test_get_general_report_by_url(self, mocker):
        """It should return True if the report exists"""
        mocker.patch(
            "src.main.python.SocialEcosystemAnalyser.database.reports.general.api_general_reports_repository.r.get",
            return_value=type("Response", (object, ), {"status_code": 200}),
        )
        assert ApiGeneralReportsRepository.get_general_report_by_url("Test")

    def test_get_general_report_by_url_no_report(self, mocker):
        """It should return False if the report does not exist"""
        mocker.patch(
            "src.main.python.SocialEcosystemAnalyser.database.reports.general.api_general_reports_repository.r.get",
            return_value=type("Response", (object, ), {"status_code": 404}),
        )
        assert not ApiGeneralReportsRepository.get_general_report_by_url(
            "Test")

    def test_add_general_report(self, mocker):
        """It should return True if the videos are added"""
        report = GeneralReport(
            id="00000",
            topic="Test",
            title="Test",
            description="Test",
            view_count="Test",
            like_count="Test",
            published_at="Test",
            urls_reports=[],
        )
        mocker.patch(
            "src.main.python.SocialEcosystemAnalyser.database.reports.general.api_general_reports_repository.r.post",
            return_value=type("Response", (object, ), {"status_code": 201}),
        )
        assert ApiGeneralReportsRepository.add_general_report(report)

    def test_add_videos_no_videos(self):
        """It should return False if no videos are added"""
        assert not ApiGeneralReportsRepository.add_general_report(None)
