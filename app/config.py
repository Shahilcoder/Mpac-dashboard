import os

from dotenv import load_dotenv

# for local
load_dotenv()

USERNAME = os.environ.get("MONGO_USER")
PASSWORD = os.environ.get("MONGO_PASSWORD")
HOST = os.environ.get("MONGO_HOST")
JWT_SECRET = os.environ.get("JWT_SECRET")
