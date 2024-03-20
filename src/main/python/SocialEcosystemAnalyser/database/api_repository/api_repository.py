import os
from abc import ABC

from dotenv import load_dotenv


class ApiRepository(ABC):
    load_dotenv()
    _api = os.environ.get("API_URL", "http://localhost:3000/")
    _token = os.environ.get("API_TOKEN", "")
