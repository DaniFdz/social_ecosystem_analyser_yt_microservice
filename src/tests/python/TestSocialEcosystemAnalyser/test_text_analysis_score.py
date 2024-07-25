import pytest

from src.main.python.SocialEcosystemAnalyser.nlp.text_analysis_score import (
    get_text_analysis_score, preprocess)


@pytest.mark.unittest
class TestTextAnalysisScore:
    def test_analysis_score(self):
        """It should return a score"""
        text = "The life is beautiful"
        output = get_text_analysis_score(text)
        assert output >= -1 and output <= 1
