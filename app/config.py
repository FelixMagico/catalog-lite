import os

from dotenv import load_dotenv

load_dotenv()  # legge il file .env


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
