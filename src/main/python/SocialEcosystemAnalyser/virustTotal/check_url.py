from virus_total_apis import PublicApi as VirusTotalPublicApi

from ..exceptions.social_ecosystem_analyser_exception import (  # type: ignore
    MessageExceptions, SocialEcosystemAnalyserException)


def check_url(api_key: str, url: str):
    vt = VirusTotalPublicApi(api_key)
    response = vt.get_url_report(url)
    if "error" in response:
        raise SocialEcosystemAnalyserException(
            MessageExceptions.VIRUSTOTAL_API_ERROR)

    malicious = any(
        [x["detected"] for x in response["results"]["scans"].values()])

    return malicious
