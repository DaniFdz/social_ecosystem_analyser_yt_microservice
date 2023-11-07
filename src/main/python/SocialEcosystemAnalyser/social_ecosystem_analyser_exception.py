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
    YOUTUBE_API_KEY_ERROR = "Invalid Youtube API key"
    YOUTUBE_API_QUOTA_EXCEEDED = "Youtube API quota exceeded"
    COHERE_API_ERROR = "Error in Cohere API"
    VIRUSTOTAL_API_ERROR = "Error in VirusTotal API"
    MONGO_CONNECTION_ERROR = "Error connecting to MongoDB"
    MONGO_CLIENT_TYPE_ERROR = "The client value must be a pymongo.MongoClient instance"
    MONGO_DB_TYPE_ERROR = "The db value must be a pymongo.database.Database instance"
    MONGO_DB_DELETE_ERROR = "Error deleting value from the database"