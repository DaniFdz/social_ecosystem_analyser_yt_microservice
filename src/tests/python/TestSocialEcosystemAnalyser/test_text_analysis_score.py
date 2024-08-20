import pytest

from src.main.python.SocialEcosystemAnalyser.nlp.text_analysis_score import \
    TextAnalysisScore


@pytest.mark.unittest
class TestTextAnalysisScore:
    def test_analysis_score(self):
        """It should return a score"""
        sa = TextAnalysisScore()
        text = "The life is beautiful"
        output = sa.get_text_analysis_score(text)
        assert output >= -1 and output <= 1
