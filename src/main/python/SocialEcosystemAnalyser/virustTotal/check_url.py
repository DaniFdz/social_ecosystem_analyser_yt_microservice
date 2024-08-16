from urllib.parse import urlparse

import requests

from src.main.python.SocialEcosystemAnalyser.database.reports.virustotal.virustotal_reports_repository import \
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
            "content-type": "application/x-www-form-urlencoded",
        }
        req_url = self.base + "urls"
        data = {"url": url}
        response = requests.post(req_url, data=data, headers=headers)

        if response.status_code != 200:
            print(f"Error in get_url_id with url: {url}, message {response.text}")
            if "QuotaExceededError" in response.text:
                raise SocialEcosystemAnalyserException(
                    MessageExceptions.VIRUSTOTAL_API_ERROR)
            else:
                return None


        return response.json()

    def get_url_report(self, url):
        headers = {"accept": "application/json", "x-apikey": self.api_key}
        req_url = self.base + "urls/" + url  # noqa
        response = requests.get(req_url, headers=headers)
        if response.status_code != 200:
            if "QuotaExceededError" in response.text:
                print(f"Error in get_url_id with url: {url}, message {response.text}")
                raise SocialEcosystemAnalyserException(
                    MessageExceptions.VIRUSTOTAL_API_ERROR)
            else:
                return None

        data = response.json()["data"]["attributes"]

        domain = urlparse(url).netloc
        return VTReport(
            data["first_submission_date"]
            if "first_submission_date" in data else 0,
            data["last_modification_date"]
            if "last_modification_date" in data else 0,
            (data["last_http_response_content_length"]
             if "last_http_response_content_length" in data else 0),
            data["tags"] if "tags" in data else [],
            data["html_meta"] if "html_meta" in data else dict(),
            data["times_submitted"] if "times_submitted" in data else 0,
            data["redirection_chain"] if "redirection_chain" in data else [],
            data["trackers"] if "trackers" in data else dict(),
            data["threat_names"] if "threat_names" in data else [],
            data["url"] if "url" in data else url,
            domain,
            data["categories"] if "categories" in data else dict(),
            data["last_analysis_stats"]
            if "last_analysis_stats" in data else dict(),
            data["reputation"] if "reputation" in data else 0,
            data["last_http_response_code"]
            if "last_http_response_code" in data else 0,
            (data["last_http_response_headers"]
             if "last_http_response_headers" in data else dict()),
        )
