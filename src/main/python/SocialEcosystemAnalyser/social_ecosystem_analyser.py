import os

from decouple import config

from .youtube.youtube_api import YoutubeAPI
from .database_management import DatabaseManagement
from .nlp.similar_topics_generation import generate_topics
from .social_ecosystem_analyser_exception import SocialEcosystemAnalyserException, MessageExceptions

YOUTUBE_API_KEY = config('YOUTUBE_API_KEY')
COHERE_API_KEY = config('COHERE_API_KEY')

def our_exit():
    """ Exit the program

        TODO: This function should be chaged entirely
    """
    os.kill(os.getpid(), 9)

    

def main():
    """ Main program function """
    database_management = DatabaseManagement()
    youtube_api = YoutubeAPI(YOUTUBE_API_KEY)

    topic = input("Enter a topic: ")
    
    try:
        topics = generate_topics(topic, COHERE_API_KEY)
    except SocialEcosystemAnalyserException as e:
        print(e)
        if input("Do you want to continue? (Y/n): ").lower() == "n":
            our_exit()
        topics = [topic]

    print(f"[i] Testing topics: {topics}")
    try:
        i = 0
        while i < len(topics):
            try:
                next_page_token = database_management.get_next_page_token()
            except TypeError:
                next_page_token = None
            
            next_page_token, videos_data = youtube_api.get_videos_data(topics[i], next_page_token)

            if next_page_token is None:
                i += 1
                if database_management.delete_next_page_token() == 0:
                    raise SocialEcosystemAnalyserException(
                        MessageExceptions.MONGO_DB_DELETE_ERROR
                    )  
            else:
                database_management.save_next_page_token(next_page_token)

            ids = database_management.add_videos(*videos_data)
            print(f"[i] Added {len(ids)} videos to the database")

    except SocialEcosystemAnalyserException as e:
        print(e)
        our_exit()

if __name__ == "__main__":
    main()
    our_exit()