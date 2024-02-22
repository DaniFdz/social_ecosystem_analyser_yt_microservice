# noqa
import os
from typing import List

import cohere
from dotenv import load_dotenv

from ..exceptions.social_ecosystem_analyser_exception import \
    SocialEcosystemAnalyserException
from ..exceptions.social_ecosystem_analyser_messages import MessageExceptions


def generate_topics(topic: str) -> List[str]:
    """
    Generate similar topics to the given topic.

    @param: topic (str): Topic to generate similar topics
    """
    load_dotenv()
    api_key = os.environ.get("COHERE_API_KEY")
    try:
        co = cohere.Client(api_key)
        response = co.generate(
            model="command",
            prompt='For each topic I want 5 similar topics:\n\n"Animals":' +
            ' "zoo,mamals,elepahnts,dogs,pet";\n"Food": "apple,tomato,hambu' +
            f'rguer,fish,meat";\n"Cities": "Madrid,Paris,New York,London,Texas";\n"{topic}":',
            max_tokens=300,
            temperature=
            1.2,  # The range is 0-2, with 0 being the most conservative and 2 being the most creative.
            k=0,
            stop_sequences=[";"],
            return_likelihoods="NONE",
        )
    except Exception as e:
        raise SocialEcosystemAnalyserException(
            MessageExceptions.COHERE_API_ERROR) from e

    response_text = response.generations[0].text.split(";")[0].replace('"', "")

    data = response_text.strip().split(",")

    # if len(data) != 5:
    #     return generate_topics(topic, api_key)

    return data
