import pytest

from src.main.python.SocialEcosystemAnalyser.database.reports.api_reports_repository import \
    ApiReportsRepository
from src.main.python.SocialEcosystemAnalyser.database.reports.reports_repository import \
    VTReport


@pytest.mark.api
@pytest.mark.unittest
class TestReport:
    def test_add_reports(self, mocker):
        """It should return True if the videos are added"""
        reports = [
            VTReport(
                first_submission_date="Test",
                last_modification_date="Test",
                last_http_response_content_length="Test",
                tags="Test",
                html_meta="Test",
                times_submitted="Test",
                redirection_chain="Test",
                trackers="Test",
                threat_names="Test",
                url="Test",
                categories="Test",
                last_analysis_stats="Test",
                reputation="Test",
                last_http_response_code="Test",
                last_http_response_headers="Test",
            )
        ]
        mocker.patch(
            "src.main.python.SocialEcosystemAnalyser.database.reports.api_reports_repository.r.post",
            return_value=type("Response", (object, ), {"status_code": 201}),
        )
        assert ApiReportsRepository.add_reports(reports)

    def test_add_videos_no_videos(self, mocker):
        """It should return False if no videos are added"""
        assert not ApiReportsRepository.add_reports([])