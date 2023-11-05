from decouple import config
from pymongo import MongoClient, errors, database

from .singleton_metaclass import SingletonMeta
from .social_ecosystem_analyser_exception \
    import SocialEcosystemAnalyserException, MessageExceptions


class DatabaseManagement(metaclass=SingletonMeta):
    def __init__ (self):
        MONGO_USERNAME = config("MONGO_USERNAME")
        MONGO_PASSWORD = config("MONGO_PASSWORD")
        MONGO_HOST = config("MONGO_HOST") 
        MONGO_PORT = config("MONGO_PORT")

        self.__client = None
        self.__db = None

        try:
            self.__client = MongoClient(
                host = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}"+\
                       f"@{MONGO_HOST}:{MONGO_PORT}/?authSource=admin",
                serverSelectionTimeoutMS=5000,
            )
        except errors.ServerSelectionTimeoutError as err:
            raise SocialEcosystemAnalyserException(
                    MessageExceptions.MONGO_CONNECTION_ERROR
                ) from err
        
        try:
            self.db = self.__client["social_ecosystem_analyser"]
        except errors.InvalidName as err:  
            raise SocialEcosystemAnalyserException(
                    MessageExceptions.MONGO_DB_NAME_ERROR
                ) from err

    def __del__(self):
        self.__client.close()


    def add_videos(self, *videos: list):
        """Add videos to the database

        Args:
            videos (list): List of videos to add to the database
        
        Returns:
            ids (list[pymongo.ObjectId]): Id's of the videos added to the database
        """
        ids = []
        for video in videos:
            ids.append(self.__db.videos.insert_one(video).inserted_id)
        return ids
            

    def get_videos(self, start: int = 0, limit: int = 0):
        """Get videos from the database

        Args:
            limit (int, optional): Limit of videos to get. Defaults to 0.

        Returns:
            list: List of videos
        """
        if limit == 0:
            return list(self.__db['videos'].find().skip(start))
        else:
            return list(self.__db['videos'].find().skip(start).limit(limit))


    def delete_videos(self, *ids: list):
        """Delete videos from the database

        Args:
            ids (list[pymongo.ObjectId]): List of videos to delete from the database
        
        Returns:
            int: Number of videos deleted
        """
        return self.__db['videos'].delete_many({"_id": {"$in": ids}}).deleted_count

    def save_next_page_token(self, token: str):
        """Save the next page token in the database, if it doesn't exist, it will be created

        Args:
            token (str): Next page token
        """
        self.__db['next_page_token'].update_one(
            {"_id": "next_page_token"},
            {"$set": {"token": token}},
            upsert=True
        )

    def get_next_page_token(self):
        """Get the next page token from the database

        Returns:
            str: Next page token
            None: If there is no next page token
        """
        return self.__db['next_page_token'].find_one()['token']
    
        
    @property
    def db(self):
        return self.__db
    
    @db.setter
    def db(self, value):
        if isinstance(value, database.Database):
            self.__db = value
        else:
            raise SocialEcosystemAnalyserException(
                    MessageExceptions.MONGO_DB_TYPE_ERROR
                )