from virus_total_apis import PublicApi as VirusTotalPublicApi

from ..social_ecosystem_analyser_exception import \
    SocialEcosystemAnalyserException, MessageExceptions

def check_url(api_key: str, url: str):
    vt = VirusTotalPublicApi(api_key)
    response = vt.get_url_report(url)
    if "error" in response:
        raise SocialEcosystemAnalyserException(
            MessageExceptions.VIRUSTOTAL_API_ERROR
        )
    
    malicious = any([x["detected"] for x in response["results"]["scans"].values()])

    return malicious