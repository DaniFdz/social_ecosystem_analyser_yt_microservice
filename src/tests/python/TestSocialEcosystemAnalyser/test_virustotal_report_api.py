import pytest

from src.main.python.SocialEcosystemAnalyser.database.reports.virustotal.api_virustotal_reports_repository import \
    ApiVirusTotalReportsRepository
from src.main.python.SocialEcosystemAnalyser.database.reports.virustotal.virustotal_reports_repository import \
    VTReport


@pytest.mark.api
@pytest.mark.unittest
class TestReport:
    def test_get_virustotal_report_by_url(self, mocker):
        """It should return True if the report exists"""
        mocker.patch(
            "src.main.python.SocialEcosystemAnalyser.database.reports.virustotal.api_virustotal_reports_repository.r.get",
            return_value=type("Response", (object, ), {
                "status_code": 200,
                "json": lambda: []
            }),
        )
        assert ApiVirusTotalReportsRepository.get_virustotal_report_by_url(
            "Test")

    def test_get_virustotal_report_by_url_no_report(self, mocker):
        """It should return False if the report does not exist"""
        mocker.patch(
            "src.main.python.SocialEcosystemAnalyser.database.reports.virustotal.api_virustotal_reports_repository.r.get",
            return_value=type("Response", (object, ), {"status_code": 404}),
        )
        assert not ApiVirusTotalReportsRepository.get_virustotal_report_by_url(
            "Test")

    def test_add_virustotal_report(self, mocker):
        """It should return True if the videos are added"""
        report = VTReport(
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
            domain="domain.com",
            categories="Test",
            last_analysis_stats="Test",
            reputation="Test",
            last_http_response_code="Test",
            last_http_response_headers="Test",
        )
        mocker.patch(
            "src.main.python.SocialEcosystemAnalyser.database.reports.virustotal.api_virustotal_reports_repository.r.post",
            return_value=type("Response", (object, ), {"status_code": 201}),
        )
        assert ApiVirusTotalReportsRepository.add_virustotal_report(report)

    def test_add_videos_no_videos(self):
        """It should return False if no videos are added"""
        assert not ApiVirusTotalReportsRepository.add_virustotal_report(None)
