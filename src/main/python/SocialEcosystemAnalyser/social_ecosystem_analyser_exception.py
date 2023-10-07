class SocialEcosystemAnalyserException(Exception):
    """Personalised exception"""
    def __init__(self, message):
        self.__message = message
        super().__init__(self.message)

    @property
    def message(self):
        """gets the message value"""
        return self.__message

    @message.setter
    def message(self, value):
        self.__message = value

class MessageExceptions:
    """MessageException class"""
    YOUTUBE_API_ERROR = "Error in Youtube API"
    MONGO_CONNECTION_ERROR = "Error connecting to MongoDB"
    MONGO_CLIENT_TYPE_ERROR = "The client value must be a pymongo.MongoClient instance"
    MONGO_DB_TYPE_ERROR = "The db value must be a pymongo.database.Database instance"