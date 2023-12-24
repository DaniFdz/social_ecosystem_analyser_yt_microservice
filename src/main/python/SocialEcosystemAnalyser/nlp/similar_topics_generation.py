import cohere

from ..social_ecosystem_analyser_exception import (
    MessageExceptions, SocialEcosystemAnalyserException)


def generate_topics(topic: str, api_key: str):
    try:
        co = cohere.Client(api_key)
        response = co.generate(
            model="command",
            prompt=
            f'For each topic I want 5 similar topics:\n\n"Animals": "zoo,mamals,elepahnts,dogs,pet";\n"{topic}":',
            max_tokens=300,
            temperature=
            1.2,  # The range is 0-2, with 0 being the most conservative and 2 being the most creative.
            k=0,
            stop_sequences=[";"],
            return_likelihoods="NONE")
    except Exception as e:
        raise SocialEcosystemAnalyserException(
            MessageExceptions.COHERE_API_ERROR) from e

    response_text = response.generations[0].text.split(";")[0].replace('"', "")

    return response_text.strip().split(",")
