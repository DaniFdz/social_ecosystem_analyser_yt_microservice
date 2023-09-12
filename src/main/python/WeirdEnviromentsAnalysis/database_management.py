from decouple import config
from pymongo import MongoClient, errors
from .singleton_metaclass import SingletonMeta
from .weird_enviroments_analysis_exception \
    import WeirdEnviromentsAnalysisException, MessageExceptions

class DatabaseManagement(metaclass=SingletonMeta):
    def __init__ (self):
        MONGO_USERNAME = config("MONGO_USERNAME")
        MONGO_PASSWORD = config("MONGO_PASSWORD")
        MONGO_HOST = config("MONGO_HOST") 
        MONGO_PORT = config("MONGO_PORT")

        self.__client = None

        try:
            self.client = MongoClient(
                host = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}"+\
                       f"@{MONGO_HOST}:{MONGO_PORT}/?authSource=admin",
                serverSelectionTimeoutMS=5000,
            )
            print("Connected to MongoDB: "+\
                  self.client.server_info()['version'])
            print(f"Available databases: {self.client.list_database_names()}")

        except errors.ServerSelectionTimeoutError as err:
            raise WeirdEnviromentsAnalysisException(
                MessageExceptions.MONGO_CONNECTION_ERROR.value
                ) from err
        
    @property
    def client(self):
        return self.__client
    
    @client.setter
    def client(self, value):
        if isinstance(value, MongoClient):
            self.__client = value
        else:
            raise WeirdEnviromentsAnalysisException(
                "The client value must be a pymongo.MongoClient instance"
                )