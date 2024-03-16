import base64

import requests

from src.main.python.SocialEcosystemAnalyser.database.reports.reports_repository import \
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

    def get_url_report(self, url):
        headers = {"accept": "application/json", "x-apikey": self.api_key}
        req_url = self.base + "urls/" + base64.b64encode(bytes(
            url, "utf-8")).decode()
        print(req_url)
        response = requests.get(req_url, headers=headers)

        if response.status_code != 200:
            raise SocialEcosystemAnalyserException(
                MessageExceptions.VIRUSTOTAL_API_ERROR)

        data = response.json()["data"]["attributes"]
        return VTReport(
            data["first_submission_date"],
            data["last_modification_date"],
            data["last_http_response_content_length"],
            data["tags"],
            data["html_meta"],
            data["times_submitted"],
            data["redirection_chain"],
            data["trackers"],
            data["threat_names"],
            data["url"],
            data["categories"],
            data["last_analysis_stats"],
            data["reputation"],
            data["last_http_response_code"],
            data["last_http_response_headers"],
        )
