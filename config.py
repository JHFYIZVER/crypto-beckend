import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("API_KEY")
    APP_URL = os.getenv("APP_URL")
    BASE_URL = os.getenv("BASE_URL")

settings = Config()