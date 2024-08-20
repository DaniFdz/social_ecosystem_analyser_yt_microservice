from time import time

import numpy as np
from scipy.special import softmax
from transformers import (AutoConfig, AutoModelForSequenceClassification,
                          AutoTokenizer, logging)


class TextAnalysisScore:
    def __init__(self):
        logging.set_verbosity_error()
        self.MODEL_NAME = f"cardiffnlp/twitter-roberta-base-sentiment-latest"

        self.tokenizer = AutoTokenizer.from_pretrained(self.MODEL_NAME)
        self.config = AutoConfig.from_pretrained(self.MODEL_NAME)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.MODEL_NAME)

    def preprocess(self, text: str) -> str:
        new_text = []
        for t in text.split(" "):
            t = "@user" if t.startswith("@") and len(t) > 1 else t
            t = "http" if t.startswith("http") else t
            new_text.append(t)
        return " ".join(new_text)


    def calculate_sentiment_score(self, classification) -> float:
        positive = classification.get("positive", 0)
        neutral = classification.get("neutral", 0)
        negative = classification.get("negative", 0)

        total = positive + neutral + negative

        if total == 0:
            return 0

        weighted_sum = positive - negative
        score = weighted_sum / total

        return float(score)

    def get_text_analysis_score(self, text: str) -> float:
        start_sa_time = time()
        text = self.preprocess(text)
        encoded_input = self.tokenizer(
            text, return_tensors="pt", max_length=512, truncation=True
        )
        output = self.model(**encoded_input)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)

        # Print labels and scores
        ranking = np.argsort(scores)
        ranking = ranking[::-1]

        classification = {
            self.model.config.id2label[ranking[i]]: scores[ranking[i]]
            for i in range(len(scores))
        }
        score = self.calculate_sentiment_score(classification)
        elapsed_sa_time = time() - start_sa_time
        print(f"Elapsed time for sentiment analysis: {elapsed_sa_time} seconds")
        print("Analyzing text... -> Score: ", score)
        return score
