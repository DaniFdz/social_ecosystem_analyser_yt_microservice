import pytest

from src.main.python.SocialEcosystemAnalyser.exceptions.social_ecosystem_analyser_exception import \
    SocialEcosystemAnalyserException
from src.main.python.SocialEcosystemAnalyser.exceptions.social_ecosystem_analyser_messages import \
    MessageExceptions


@pytest.mark.database
@pytest.mark.unittest
class TestDatabaseManagement:
    single_item = [{"test": "test"}]
    multiple_items = [{"test": "test"}, {"test": "test"}]

    def test_init(self, database_management):
        """Test if database management is initialized correctly"""
        assert database_management is not None

    def test_add_video(self, database_management):
        """Test if a video is added correctly to the database"""
        ids = database_management.add_videos(*self.single_item)
        assert ids is not None
        assert len(ids) == 1
        database_management.delete_videos(*ids)

    def test_add_videos(self, database_management):
        """Test if videos are added correctly to the database"""
        ids = database_management.add_videos(*self.multiple_items)
        assert ids is not None
        assert len(ids) == 2
        database_management.delete_videos(*ids)

    def test_get_video(self, database_management):
        """Test if a video is retrieved correctly from the database"""
        ids = database_management.add_videos(*self.single_item)
        result = database_management.get_videos()
        assert result is not None
        assert list(self.single_item[0].items())[0] in result[-1].items()
        database_management.delete_videos(*ids)

    def test_get_videos_limit(self, database_management):
        """Test if videos are retrieved correctly from the database with a limit"""
        ids = database_management.add_videos(*self.multiple_items)
        videos = database_management.get_videos(start=1, limit=1)
        database_management.delete_videos(*ids)
        assert len(videos) == 1

    def test_delete_video(self, database_management):
        """Test if a video is deleted correctly from the database"""
        ids = database_management.add_videos(*self.single_item)
        assert database_management.delete_videos(*ids) == 1

    def test_delete_videos(self, database_management):
        """Test if videos are deleted correctly from the database"""
        ids = database_management.add_videos(*self.multiple_items)
        assert database_management.delete_videos(*ids) == 2

    def test_save_and_get_next_page_token(self, database_management):
        """Test if the next page token is saved correctly to the database"""
        database_management.save_next_page_token("topic", "token")
        next_page_token = database_management.get_next_page_token("topic")
        database_management.db["next_page_topic"].delete_one(
            {"_id": "next_page_token_topic"})
        assert next_page_token == "token"

    def test_overwrite_next_page_token(self, database_management):
        """Test if the next page token is overwritten correctly in the database"""
        database_management.save_next_page_token("topic_", "token")
        database_management.save_next_page_token("topic_", "new_token")
        next_page_token = database_management.get_next_page_token("topic_")
        database_management.db["next_page_topic_"].delete_one(
            {"_id": "next_page_token_topic"})
        assert next_page_token == "new_token"

    def test_db(self, database_management):
        """Test if the db value is retrieved correctly"""
        assert database_management.db is not None

    def test_set_db_error(self, database_management):
        """Test if the db value is set correctly"""
        with pytest.raises(SocialEcosystemAnalyserException,
                           match=MessageExceptions.MONGO_DB_TYPE_ERROR):
            database_management.db = None
