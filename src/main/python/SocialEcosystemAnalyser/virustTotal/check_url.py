from urllib.parse import urlparse

import requests

from src.main.python.SocialEcosystemAnalyser.database.reports.virustotal_reports_repository import \
    VTReport
from src.main.python.SocialEcosystemAnalyser.exceptions.social_ecosystem_analyser_exception import \
    SocialEcosystemAnalyserException
from src.main.python.SocialEcosystemAnalyser.exceptions.social_ecosystem_analyser_messages import \
    MessageExceptions


class VTApi:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.version = 3
        self.base = f"https://www.virustotal.com/api/v{self.version}/"
        if api_key is None:
            raise SocialEcosystemAnalyserException(
                MessageExceptions.VIRUSTOTAL_API_KEY_NOT_FOUND)

    def get_url_id(self, url):
        headers = {
            "accept": "application/json",
            "x-apikey": self.api_key,
            "content-type": "application/x-www-form-urlencoded"
        }
        req_url = (self.base + "urls")
        data = {"url": url}
        response = requests.post(req_url, data=data, headers=headers)

        if response.status_code != 200:
            print(response.text)
            raise SocialEcosystemAnalyserException(
                MessageExceptions.VIRUSTOTAL_API_ERROR)

        return response.json()

    def get_url_report(self, url):
        print(url)
        headers = {"accept": "application/json", "x-apikey": self.api_key}
        req_url = (
            self.base + "urls/"  # noqa:
            + url  # noqa:
        )
        response = requests.get(req_url, headers=headers)
        if response.status_code != 200:
            print(response.text)
            if "NotFoundError" in response.text:
                return None
            raise SocialEcosystemAnalyserException(
                MessageExceptions.VIRUSTOTAL_API_ERROR)

        data = response.json()["data"]["attributes"]

        domain = urlparse(url).netloc
        return VTReport(
            data["first_submission_date"],
            data["last_modification_date"],
            data["last_http_response_content_length"]
            if "last_http_response_content_length" in data else [],
            data["tags"],
            data["html_meta"] if "html_meta" in data else [],
            data["times_submitted"],
            data["redirection_chain"] if "redirection_chain" in data else [],
            data["trackers"] if "trackers" in data else [],
            data["threat_names"],
            data["url"],
            domain,
            data["categories"],
            data["last_analysis_stats"],
            data["reputation"],
            data["last_http_response_code"],
            data["last_http_response_headers"],
        )
