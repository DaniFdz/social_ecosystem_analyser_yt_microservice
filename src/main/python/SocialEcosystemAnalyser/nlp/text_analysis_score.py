import numpy as np
from scipy.special import softmax
from transformers import (AutoConfig, AutoModelForSequenceClassification,
                          AutoTokenizer)


# Preprocess text
def preprocess(text):
    new_text = []
    for t in text.split(" "):
        t = "@user" if t.startswith("@") and len(t) > 1 else t
        t = "http" if t.startswith("http") else t
        new_text.append(t)
    return " ".join(new_text)


MODEL = f"cardiffnlp/twitter-roberta-base-sentiment-latest"


def calculate_sentiment_score(classification):
    positive = classification.get('positive', 0)
    neutral = classification.get('neutral', 0)
    negative = classification.get('negative', 0)

    total = positive + neutral + negative

    if total == 0:
        return 0

    weighted_sum = positive - negative
    score = weighted_sum / total

    return float(score)


def get_text_analysis_score(text: str) -> float:
    """
    Given a text, returns its score being:
    -1 -> Negative; 0 -> Neutral; 1 -> Positive
    """
    # if text == '':
    #     return 0

    # model = pipeline('sentiment-analysis',
    #                  model='cardiffnlp/twitter-roberta-base-sentiment-latest')
    # result = model(text)

    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    config = AutoConfig.from_pretrained(MODEL)
    # PT
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)
    text = preprocess(text)
    encoded_input = tokenizer(text,
                              return_tensors="pt",
                              max_length=512,
                              truncation=True)
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)

    # Print labels and scores
    ranking = np.argsort(scores)
    ranking = ranking[::-1]

    classification = {
        model.config.id2label[ranking[i]]: scores[ranking[i]]
        for i in range(len(scores))
    }
    return calculate_sentiment_score(classification)
