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
        values = [
            {
                "name": "topic1",
                "finished": False,
                "next_page_token": None
            },
            {
                "name": "topic2",
                "finished": False,
                "next_page_token": None
            },
        ]
        topic_values = list(
            map(
                lambda x: Topic(x["name"], x["finished"], x["next_page_token"]
                                ), values))
        mocker.patch(
            "src.main.python.SocialEcosystemAnalyser.database.topics.api_topics_repository.r.get",
            return_value=type("Response", (object, ), {
                "status_code": 200,
                "json": lambda: values
            }),
        )

        assert ApiTopicsRepository.get_topics() == topic_values

    def test_create_topic(self, mocker):
        """It should create a topic and return True if the API returns 201"""
        mocker.patch(
            "src.main.python.SocialEcosystemAnalyser.database.topics.api_topics_repository.r.post",
            return_value=type("Response", (object, ), {"status_code": 201}),
        )
        assert ApiTopicsRepository.create_topic("topic")

    def test_create_topic_error(self, mocker):
        """It should return False if the API returns an error"""
        mocker.patch(
            "src.main.python.SocialEcosystemAnalyser.database.topics.api_topics_repository.r.post",
            return_value=type("Response", (object, ), {"status_code": 500}),
        )
        assert not ApiTopicsRepository.create_topic("topic")

    def test_get_topic_by_name(self, mocker):
        """It should return a topic if the API returns 200"""
        value = {"name": "topic", "finished": False, "next_page_token": None}
        topic_value = Topic(value["name"], value["finished"],
                            value["next_page_token"])
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
        topic = Topic("topic", False, None)
        mocker.patch(
            "src.main.python.SocialEcosystemAnalyser.database.topics.api_topics_repository.r.put",
            return_value=type("Response", (object, ), {"status_code": 200}),
        )
        assert ApiTopicsRepository.set_topic_as_finished(topic)

    def test_set_topic_as_finished_error(self, mocker):
        """It should return False if the API returns an error"""
        topic = Topic("topic", False, None)
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
        assert ApiTopicsRepository.save_next_page_token(topic_name, "")

    def test_save_next_page_token_error(self, mocker):
        """It should return False if the API returns an error"""
        topic_name = "topic"
        mocker.patch(
            "src.main.python.SocialEcosystemAnalyser.database.topics.api_topics_repository.r.put",
            return_value=type("Response", (object, ), {"status_code": 404}),
        )
        assert not ApiTopicsRepository.save_next_page_token(topic_name, "")
