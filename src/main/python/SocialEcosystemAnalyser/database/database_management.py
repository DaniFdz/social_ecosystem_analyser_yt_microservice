import os
from typing import Any, List

from pymongo import MongoClient, database, errors

from src.main.python.SocialEcosystemAnalyser.exceptions.social_ecosystem_analyser_exception import \
    SocialEcosystemAnalyserException
from src.main.python.SocialEcosystemAnalyser.exceptions.social_ecosystem_analyser_messages import \
    MessageExceptions
from src.main.python.SocialEcosystemAnalyser.utils.singleton_metaclass import \
    SingletonMeta


class DatabaseManagement(metaclass=SingletonMeta):
    """
    Class to manage database operations.

    It uses the Singleton pattern to ensure that only one instance of the class is created.

    It's important to close the connection of the database when the class is destroyed
    It can be done by using the __del__ method

    @param: test (bool, optional): If the database is for testing. Defaults to False.
    """
    def __init__(self, test=False):
        MONGO_USERNAME = os.environ.get("MONGO_USERNAME")
        MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")
        MONGO_HOST = os.environ.get("MONGO_HOST")
        MONGO_PORT = os.environ.get("MONGO_PORT")

        self.__client = None
        self.__db = None

        try:
            self.__client = MongoClient(
                host=
                f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/?authSource=admin",
                serverSelectionTimeoutMS=5000,
            )
        except errors.ServerSelectionTimeoutError as err:
            raise SocialEcosystemAnalyserException(
                MessageExceptions.MONGO_CONNECTION_ERROR) from err

        if test:
            self.db = self.__client["social_ecosystem_analyser_testing"]
        else:
            self.db = self.__client["social_ecosystem_analyser"]

    def __del__(self) -> None:
        """Close the connection of the database when the class is destroyed"""
        self.__client.close()

    def add_videos(self, *videos: list) -> List[str]:
        """Add videos to the database

        @param: videos (list): List of videos to add to the database

        @return: ids (list[str]): Id"s of the videos added to the database
        """
        ids = []
        for video in videos:
            ids.append(self.__db.videos.insert_one(video).inserted_id)
        return ids

    def get_videos(self, start: int = 0, limit: int = 0) -> List[Any]:
        """Get videos from the database

        @param: start (int, optional): Start of videos to get. Defaults to 0.
        @param: limit (int, optional): Limit of videos to get. Defaults to 0.

        @return: list: List of videos
        """
        if limit == 0:
            return list(self.__db["videos"].find().skip(start))
        else:
            return list(self.__db["videos"].find().skip(start).limit(limit))

    def delete_videos(self, *ids: list):
        """Delete videos from the database

        @param: *ids (list[pymongo.ObjectId]): Id's of the videos to delete from the database

        @return: int: Number of videos deleted
        """
        return self.__db["videos"].delete_many({
            "_id": {
                "$in": ids
            }
        }).deleted_count

    def save_next_page_token(self, topic: str, token: str) -> None:
        """Save the next page token in the database, if it doesn"t exist, it will be created
        and if it exists, it will be updated

        @param: token (str): Next page token
        """
        self.db["next_page_token"].update_one(
            {"_id": f"next_page_token_{topic}"}, {"$set": {
                "token": token
            }},
            upsert=True)

    def get_next_page_token(self, topic) -> str | None:
        """Get the next page token from the database

        @return: str: Next page token
        @return: None: If there is no next page token
        """
        return self.db["next_page_token"].find_one(
            {"_id": f"next_page_token_{topic}"})["token"]

    @property
    def db(self) -> database.Database:
        """Getter for the db value"""
        return self.__db

    @db.setter
    def db(self, value) -> None:
        """Setter for the db value"""
        if isinstance(value, database.Database):
            self.__db = value
        else:
            raise SocialEcosystemAnalyserException(
                MessageExceptions.MONGO_DB_TYPE_ERROR)
