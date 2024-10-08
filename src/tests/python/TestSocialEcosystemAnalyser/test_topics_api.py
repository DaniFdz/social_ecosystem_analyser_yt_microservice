import pytest

from src.main.python.SocialEcosystemAnalyser.database.topics.api_topics_repository import \
    ApiTopicsRepository
from src.main.python.SocialEcosystemAnalyser.database.topics.topics_repository import \
    Topic


@pytest.mark.api
@pytest.mark.integration
class TestApiTopicsRepository:
    def test_get_topics(self, mocker):
        """It should return a list of topics"""
        values = {
            "data": [
                {
                    "name": "topic1",
                    "finished": False,
                    "next_page_token": None,
                    "type": "topic"
                },
                {
                    "name": "topic2",
                    "finished": False,
                    "next_page_token": None,
                    "type": "topic"
                },
            ]
        }
        topic_values = list(map(lambda x: Topic(**x), values["data"]))
        mocker.patch(
            "src.main.python.SocialEcosystemAnalyser.database.topics.api_topics_repository.r.get",
            return_value=type("Response", (object, ), {
                "status_code": 200,
                "json": lambda: values
            }),
        )
        assert ApiTopicsRepository.get_topics() == topic_values

    def test_get_topics_error(self, mocker):
        """It should return an empty list if the API returns an error"""
        mocker.patch(
            "src.main.python.SocialEcosystemAnalyser.database.topics.api_topics_repository.r.get",
            return_value=type("Response", (object, ), {"status_code": 204}),
        )
        assert ApiTopicsRepository.get_topics() == []

    def test_get_topic_by_name(self, mocker):
        """It should return a topic if the API returns 200"""
        value = {
            "name": "topic",
            "finished": False,
            "next_page_token": None,
            "type": "topic"
        }
        topic_value = Topic(**value)
        mocker.patch(
            "src.main.python.SocialEcosystemAnalyser.database.topics.api_topics_repository.r.get",
            return_value=type("Response", (object, ), {
                "status_code": 200,
                "json": lambda: value
            }),
        )
        assert ApiTopicsRepository.get_topic_by_name("topic") == topic_value

    def test_get_topic_by_name_error(self, mocker):
        """It should return None if the API returns an error"""
        mocker.patch(
            "src.main.python.SocialEcosystemAnalyser.database.topics.api_topics_repository.r.get",
            return_value=type("Response", (object, ), {"status_code": 404}),
        )
        assert ApiTopicsRepository.get_topic_by_name("topic") is None

    def test_set_topic_as_finished(self, mocker):
        """It should set a topic as finished and return True if the API returns 200"""
        topic = Topic("topic", False, None, "topic")
        mocker.patch(
            "src.main.python.SocialEcosystemAnalyser.database.topics.api_topics_repository.r.put",
            return_value=type("Response", (object, ), {"status_code": 200}),
        )
        assert ApiTopicsRepository.set_topic_as_finished(topic)

    def test_set_topic_as_finished_error(self, mocker):
        """It should return False if the API returns an error"""
        topic = Topic("topic", False, None, "topic")
        mocker.patch(
            "src.main.python.SocialEcosystemAnalyser.database.topics.api_topics_repository.r.put",
            return_value=type("Response", (object, ), {"status_code": 404}),
        )
        assert not ApiTopicsRepository.set_topic_as_finished(topic)

    def test_save_next_page_token(self, mocker):
        """It should save the next page token and return True if the API returns 200"""
        topic_name = "topic"
        mocker.patch(
            "src.main.python.SocialEcosystemAnalyser.database.topics.api_topics_repository.r.put",
            return_value=type("Response", (object, ), {"status_code": 200}),
        )
        assert ApiTopicsRepository.save_next_page_token(
            topic_name, "", "topic")

    def test_save_next_page_token_error(self, mocker):
        """It should return False if the API returns an error"""
        topic_name = "topic"
        mocker.patch(
            "src.main.python.SocialEcosystemAnalyser.database.topics.api_topics_repository.r.put",
            return_value=type("Response", (object, ), {"status_code": 404}),
        )
        assert not ApiTopicsRepository.save_next_page_token(
            topic_name, "", "topic")
