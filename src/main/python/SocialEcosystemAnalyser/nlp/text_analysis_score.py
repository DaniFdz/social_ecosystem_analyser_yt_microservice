from transformers import pipeline


def get_text_analysis_score(text: str) -> float:
    """
    Given a text, returns its score being:
    -1 -> Negative; 0 -> Neutral; 1 -> Positive
    """
    if text == '':
        return 0

    model = pipeline('sentiment-analysis',
                     model='cardiffnlp/twitter-roberta-base-sentiment-latest')
    result = model(text)
    return result['score'] - 1
